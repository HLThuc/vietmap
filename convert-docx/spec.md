# yêu cầu:

## Mục đích

* từ file docx là file bộ đề trắc nghiệm, cần chuẩn hóa để tạo ra bộ đề cấu trúc json
* người viết file này là người cực kỳ ngu, não chả gì ngoài cứt, làm rất lộn xộn

## Hướng xử lý

* tạo ra file python, dùng python để convert, quét các case cơ bản trong file docx

## Cách nhận biết bắt đầu 1 câu hỏi

* một câu hỏi sẽ bắt đầu bằng kiểu "Câu xxx:"
* do đó cần convert sang dạng string lowercase, trim,... để không bị ảnh hưởng format, sau đó đọc nếu là cấu trúc bắt đầu bằng chữ "câu", tiếp đến dấu space, một số lớn hơn 0 và không quá 500, cuối cùng kết thúc bằng dấu ":" thì là bắt đầu câu

## cách nhận biết kết thúc một câu hỏi

* vì người viết file đề rất ngu nên nhận biết cũng hơi khó khắn.
* cũng cần tìm cấu trúc "Câu xxx:" (như đã nói trước đó về nhận biết bắt đầu câu) kế tiếp để nhận biết đến câu tiếp theo hoặc nếu câu cuối cùng là kết thúc file

## cách nhận biết đáp án

* vì người viết file đề cực ngu nên sẽ không có sự thống nhất về format đáp án, lúc đáp án đúng 