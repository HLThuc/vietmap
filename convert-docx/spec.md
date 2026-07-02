## Purpose

* Convert a docx file containing a multiple-choice quiz into a JSON structure.

## Handling Approach

* Create a python file to perform the conversion and scan basic cases within the docx file.

## How to Recognize the Start of a Question

* A question will start with "Câu xxx:".
* Therefore, convert it to lowercase string, trim,... to avoid being affected by format. Then read if it follows the structure starting with the word "question", followed by a space, a number greater than 0 but not more than 100, and finally ends with ":".

## How to Recognize the End of a Question

* Also need to find the structure "Câu xxx:" (as explained earlier regarding recognizing the start of a question) next to recognize the next question or if the last question ends with the end of the file.

## How to Recognize Answers

* The answer will use a bullet, begin with *A.*, *B.*,... and may have 2 or 4 options. (note, last bullet will not be question, that is righ answear and begin with format "Đáp án:")

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

