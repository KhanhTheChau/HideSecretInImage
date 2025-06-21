# StegoRSA-HideSecretInImage - Ứng dụng giấu tin trong ảnh bằng LSB kết hợp mã hóa RSA 

StegoRSA-HideSecretInImage là một ứng dụng đơn giản viết bằng Python 3.10, cho phép bạn:
- Mã hóa thông điệp bí mật bằng thuật toán **RSA**
- Giấu thông điệp đó vào **ảnh PNG/BMP** bằng kỹ thuật **LSB (Least Significant Bit)**
- Trích xuất và giải mã lại thông điệp từ ảnh

## Tính năng chính
- Mã hóa/giải mã nội dung bằng RSA 2048-bit
- Giấu nội dung mã hóa vào ảnh mà không làm thay đổi rõ rệt
- Giải trích dữ liệu từ ảnh và giải mã lại bằng private key
- Hỗ trợ ảnh định dạng `.png` và `.bmp`

## Cài đặt

```bash
git clone https://github.com/yourusername/HideSecretInImage.git
cd HideSecretInImage
pip install -r requirements.txt
python main.py
```

## Ghi chú
- Không nên dùng ảnh .jpg vì ảnh bị nén, gây mất dữ liệu LSB.
- Có thể mở rộng sang GUI (Tkinter, PyQt, Flask) hoặc kết hợp AES để hỗ trợ giấu file lớn.