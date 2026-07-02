import argparse
import json
import os
import re

from docx import Document

QUESTION_START_RE = re.compile(r'^\s*c(?:âu|au)\s*(\d{1,3})\s*[:\.]', re.I | re.MULTILINE)
OPTION_LABEL_RE = re.compile(r'([ABCDE])\s*\.\s*')
EXPLICIT_ANSWER_RE = re.compile(r'(?:đáp\s*án|ans(?:wer)?|correct)\s*[:\-]?\s*([ABCDE])', re.I)


def is_question_start(text):
    return QUESTION_START_RE.match(text.strip()) is not None


def normalize_question_text(text):
    return text.strip()


def paragraph_to_dict(paragraph):
    runs = []
    for run in paragraph.runs:
        text = run.text or ''
        if not text:
            continue
        bold = bool(run.bold)
        runs.append({'text': text, 'bold': bold})

    is_list = False
    if paragraph._p is not None and paragraph._p.pPr is not None and paragraph._p.pPr.numPr is not None:
        is_list = True

    return {'text': paragraph.text or '', 'runs': runs, 'is_list': is_list}


def paragraph_has_option_label(text):
    return bool(OPTION_LABEL_RE.match(text.strip()))


def slice_paragraph(paragraph, start, end):
    if start >= end:
        return None
    sliced_runs = []
    cursor = 0

    for run in paragraph['runs']:
        run_text = run['text']
        run_len = len(run_text)
        run_start = cursor
        run_end = cursor + run_len
        if run_end <= start:
            cursor = run_end
            continue
        if run_start >= end:
            break
        segment_start = max(start - run_start, 0)
        segment_end = min(end - run_start, run_len)
        if segment_start < segment_end:
            sliced_runs.append({
                'text': run_text[segment_start:segment_end],
                'bold': run['bold'],
            })
        cursor = run_end

    return {'text': paragraph['text'][start:end], 'runs': sliced_runs}


def split_paragraph_by_question_markers(paragraph):
    text = paragraph['text']
    matches = list(QUESTION_START_RE.finditer(text))
    if not matches:
        return [paragraph]

    segments = []
    positions = [m.start() for m in matches] + [len(text)]
    if positions[0] > 0:
        lead_segment = slice_paragraph(paragraph, 0, positions[0])
        if lead_segment and lead_segment['text'].strip():
            segments.append(lead_segment)

    for idx in range(len(matches)):
        segment = slice_paragraph(paragraph, positions[idx], positions[idx + 1])
        if segment and segment['text'].strip():
            segments.append(segment)

    return segments


def build_combined_block(paragraphs):
    composite_text = []
    run_spans = []
    offset = 0

    for idx, paragraph in enumerate(paragraphs):
        if idx > 0:
            composite_text.append('\n')
            offset += 1

        for run in paragraph['runs']:
            text = run['text']
            if not text:
                continue
            start = offset
            end = offset + len(text)
            run_spans.append({'start': start, 'end': end, 'bold': run['bold']})
            offset = end
            composite_text.append(text)

    return ''.join(composite_text), run_spans


def build_option_spans(text, relative_offset=0):
    matches = list(OPTION_LABEL_RE.finditer(text))
    spans = []
    for index, match in enumerate(matches):
        start_local = match.start()
        end_local = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        span_text = text[start_local:end_local].strip()
        spans.append({
            'label': match.group(1).upper(),
            'start': relative_offset + start_local,
            'end': relative_offset + end_local,
            'text': span_text,
        })
    return spans


def extract_options_from_paragraphs(paragraphs):
    options = []
    label_ord = ord('A')

    for paragraph in paragraphs:
        text = paragraph['text'].strip()
        if not text:
            continue

        label_match = OPTION_LABEL_RE.match(text)
        if label_match:
            option_text = text
        else:
            option_text = f"{chr(label_ord)}. {text}"
            label_ord += 1

        options.append(option_text)

    return options


def find_explicit_answer(text):
    match = EXPLICIT_ANSWER_RE.search(text)
    if not match:
        return None
    return match.group(1).upper()


def choose_answer_indices(options, explicit_answer=None):
    if not options:
        return [-1]

    if explicit_answer:
        index = ord(explicit_answer) - ord('A')
        if 0 <= index < len(options):
            return [index]

    return [-1]


def parse_question_block(block):
    header = block['header']['text']
    paragraphs = block['paragraphs']
    composite_text, run_spans = build_combined_block(paragraphs)

    header_body = normalize_question_text(header)
    remainder_full = composite_text[len(header):]
    remainder = remainder_full.lstrip('\n ').rstrip()

    if not remainder.strip():
        question_body = header_body
        option_spans = []
    else:
        first_option = OPTION_LABEL_RE.search(remainder_full)
        if first_option:
            stem_text = remainder_full[: first_option.start()].strip()
            option_text = remainder_full[first_option.start() :].rstrip()
            question_body = header_body if not stem_text else f"{header_body}\n{stem_text}"
            option_spans = build_option_spans(option_text, relative_offset=len(header) + first_option.start())
        else:
            option_candidates = []
            for paragraph in paragraphs[1:]:
                if paragraph['text'].strip() and not is_question_start(paragraph['text']):
                    option_candidates.append(paragraph)

            if 2 <= len(option_candidates) <= 4 and all(
                paragraph_has_option_label(p['text']) or p['is_list'] for p in option_candidates
            ):
                question_body = header_body
                options = extract_options_from_paragraphs(option_candidates)
                explicit_answer = find_explicit_answer(remainder_full)
                answer_indices = choose_answer_indices(options, explicit_answer)
                return question_body.strip(), options, answer_indices
            else:
                question_body = f"{header_body}\n{remainder.strip()}" if remainder.strip() else header_body
                option_spans = []

    explicit_answer = find_explicit_answer(remainder_full)
    answer_indices = choose_answer_indices(option_spans, explicit_answer)
    options = [opt['text'] for opt in option_spans]

    if options:
        cleaned_options = []
        for opt in options:
            cleaned_opt = re.sub(r'\s*(?:\n|\r\n)?(?:đáp\s*án|ans(?:wer)?|correct)\s*[:\-]?\s*[ABCDE]\s*$', '', opt, flags=re.I).strip()
            cleaned_options.append(cleaned_opt)
        options = cleaned_options

    if question_body:
        question_body = re.sub(r'\s*(?:\n|\r\n)?(?:đáp\s*án|ans(?:wer)?|correct)\s*[:\-]?\s*[ABCDE]\s*$', '', question_body, flags=re.I).strip()

    return question_body.strip(), options, answer_indices


def collect_question_blocks(document):
    paragraph_dicts = []
    for paragraph in document.paragraphs:
        paragraph_dict = paragraph_to_dict(paragraph)
        if not paragraph_dict['text'].strip():
            continue
        for segment in split_paragraph_by_question_markers(paragraph_dict):
            if segment and segment['text'].strip():
                paragraph_dicts.append(segment)

    blocks = []
    current = None
    for paragraph in paragraph_dicts:
        text = paragraph['text'].strip()
        if is_question_start(text):
            if current:
                blocks.append(current)
            current = {'header': paragraph, 'paragraphs': [paragraph]}
        elif current:
            current['paragraphs'].append(paragraph)

    if current:
        blocks.append(current)

    return blocks


def convert_docx_to_json(input_path, output_path):
    document = Document(input_path)
    blocks = collect_question_blocks(document)
    questions = []
    for index, block in enumerate(blocks, start=1):
        question, options, answer_indices = parse_question_block(block)
        if not options:
            continue
        questions.append(
            {
                'id': index,
                'question': question,
                'options': options,
                'answer': [i for i in answer_indices] if answer_indices != [-1] else [-1],
            }
        )

    result = {'quiz1': questions}

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as out_file:
        json.dump(result, out_file, ensure_ascii=False, indent=4)


def main():
    input_path = "/home/ttb/projects/vietmap/input/file_input.docx"
    output_path = "/home/ttb/projects/vietmap/output/file_output.json"
    convert_docx_to_json(input_path, output_path)


if __name__ == '__main__':
    main()
