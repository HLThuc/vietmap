## Purpose

* Convert a docx file containing a multiple-choice quiz into a JSON structure.
* The person who wrote this file is extremely incompetent, so it's very messy.

## Handling Approach

* Create a python file to perform the conversion and scan basic cases within the docx file.

## How to Recognize the Start of a Question

* A question will start with "Câu xxx:".
* Therefore, convert it to lowercase string, trim,... to avoid being affected by format. Then read if it follows the structure starting with the word "question", followed by a space, a number greater than 0 but not more than 500, and finally ends with ":".

## How to Recognize the End of a Question

* Since the person who wrote the quiz file is very incompetent, recognition can be somewhat tricky.
* Also need to find the structure "Câu xxx:" (as explained earlier regarding recognizing the start of a question) next to recognize the next question or if the last question ends with the end of the file.

## How to Recognize Answers

* The answer will begin with *A.*, *B.*,... and may have 2 or 4 options. Read until the end of the sentence (either the beginning of the next question or the end of the file) within each sentence, there are signals indicating the correct answer. Sometime it's word typed, but some other time it's a bullet *A.*, *B.*,...
* The answear in a question must be 2 or 4 options. Read until the end of the sentence (either the beginning of the next question or the end of the file) within each sentence, there are signals indicating the correct answer.
* Since the person who wrote the quiz file is extremely incompetent, they will not have a standardized format for answers, sometimes it will be in bold letters, other times in normal letters but colored red.
* Check bold letters: use loop and check wether the answer is in normal or bold letters. If it's not in bold letters, then it's wrong. If all of the answear are normal letters, then it's wrong, let's do next checking. Note: remember that the question will can be bold letter also, therefore u must check this case and don't add the `question` into the `answear` 
* Check red color: use loop and check wether the answer is in red or not. If it's not in red, then it's wrong. If all of the answear are red or normal letters, then it's wrong, place the right answear to `-1`, i will checking it later.

## Output Format Requirement

* Need a JSON with the following format:

```json
{
    "quiz1": [
        {
            "id": 1,
            "question": "(1) C\u00e1c tri\u1ec7u ch\u1ee9ng nhi\u1ec5m tr\u00f9ng \u1edf ng\u01b0\u1eddi gi\u00e0 bi\u1ec3u hi\u1ec7n r\u1ea5t \u0111\u1eb7c tr\u01b0ng v\u00ec (2) c\u01a1 ch\u1ebf mi\u1ec5n d\u1ecbch \u1edf ng\u01b0\u1eddi gi\u00e0 k\u00e9m h\u01a1n \u1edf nh\u1eefng ng\u01b0\u1eddi tr\u1ebb:",
            "options": [
                "A. (1) \u0111\u00fang (2) \u0111\u00fang; (1) v\u00e0 (2) c\u00f3 li\u00ean quan nh\u00e2n qu\u1ea3",
                "B. (1) \u0111\u00fang, (2) \u0111\u00fang; (1) v\u00e0 (2) kh\u00f4ng c\u00f3 li\u00ean quan nh\u00e2n qu\u1ea3",
                "C. (1) \u0111\u00fang (2) sai",
                "D. (1) sai (2) \u0111\u00fang"
            ],
            "answer": 3
        },
        ...
    ]
}
```

* in which quiz1 is unique and fixed
* need to create a python file converter.py located in the convert-docx directory to process data from the json file
* when running this python file and modifying the input + output dir, it will produce:
    * The input file will be in the input directory of the project
    * The output file will be in the output directory of the project

