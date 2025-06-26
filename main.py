from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
from rsa import generate_keys, encrypt_to_binary, decrypt_from_binary, embed_text_lsb, extract_text_lsb

# === GIAO DIỆN ===
window = Tk()
window.title("Ứng dụng giấu tin trong ảnh bằng LSB kết hợp mã hóa RSA")
selected_image_path = None
image_array = None
binary_data = ''
private_key = None
public_key = None

preview_label = None
result_image_label = None

def upload_image():
    global selected_image_path, image_array, preview_label
    filepath = filedialog.askopenfilename(title="Chọn ảnh để giấu tin", filetypes=[("Image files", "*.png *.bmp")])
    if filepath:
        selected_image_path = filepath
        pil_img = Image.open(filepath).convert("RGB")
        image_array = np.array(pil_img)

        pil_img.thumbnail((300, 300))
        img_tk = ImageTk.PhotoImage(pil_img)
        if preview_label:
            preview_label.config(image=img_tk)
            preview_label.image = img_tk
        else:
            preview_label = Label(window, image=img_tk)
            preview_label.image = img_tk
            preview_label.grid(column=2, row=2, rowspan=10, padx=20, pady=10)

def create_keys():
    global private_key, public_key
    public_key, private_key = generate_keys(bits=16)  # dùng 16 bit để thao tác nhanh
    pub_key.delete('1.0', END)
    pri_key.delete('1.0', END)
    pub_key.insert(END, str(public_key))
    pri_key.insert(END, str(private_key))

def encrypt_text():
    global binary_data
    message = Initialtxt.get()
    if not message or not public_key:
        return
    binary_data = encrypt_to_binary(message, public_key)
    RESULT_ENCODE.delete(0, END)
    RESULT_ENCODE.insert(END, binary_data)

def decrypt_text():
    global binary_data
    if not binary_data or not private_key:
        return
    try:
        decrypted = decrypt_from_binary(binary_data, private_key)
        RESULT_DECODE.delete(0, END)
        RESULT_DECODE.insert(END, decrypted)
    except Exception as e:
        RESULT_DECODE.delete(0, END)
        RESULT_DECODE.insert(END, f"Lỗi: {e}")

def embed_data():
    global binary_data, image_array, result_image_label
    if image_array is None or not binary_data:
        status_label.config(text="❌ Chưa có ảnh hoặc dữ liệu để chèn", fg="red")
        return
    try:
        modified = embed_text_lsb(image_array.copy(), binary_data)
        cv2.imwrite('result.png', cv2.cvtColor(modified, cv2.COLOR_RGB2BGR))
        status_label.config(text="✅ Đã giấu tin vào ảnh result.png", fg="green")
        RESULT_ENCODE.insert(END, " | ✅")

        # Hiển thị ảnh kết quả
        pil_result = Image.fromarray(modified)
        pil_result.thumbnail((300, 300))
        result_imgtk = ImageTk.PhotoImage(pil_result)

        if result_image_label:
            result_image_label.config(image=result_imgtk)
            result_image_label.image = result_imgtk
        else:
            result_image_label = Label(window, image=result_imgtk)
            result_image_label.image = result_imgtk
            result_image_label.grid(column=2, row=13, padx=20, pady=10)

    except Exception as e:
        status_label.config(text=f"❌ Lỗi khi giấu tin: {e}", fg="red")
        RESULT_ENCODE.insert(END, f" | ❌ Lỗi: {e}")

def extract_and_decrypt():
    global private_key
    if image_array is None or not private_key:
        return
    try:
        result_img = cv2.cvtColor(cv2.imread('result.png'), cv2.COLOR_BGR2RGB)
        recovered = extract_text_lsb(result_img, len(binary_data))
        decrypted = decrypt_from_binary(recovered, private_key)
        RESULT_DECODE.delete(0, END)
        RESULT_DECODE.insert(END, decrypted)
    except Exception as e:
        RESULT_DECODE.delete(0, END)
        RESULT_DECODE.insert(END, f"❌ Lỗi: {e}")

# === GIAO DIỆN THÀNH PHẦN ===
Label(window, text="🔐 RSA + 🖼️ LSB Steganography", font=("Arial Bold", 22), fg="blue").grid(column=1, row=0, pady=10)
Label(window, text="Giấu tin an toàn bằng kỹ thuật mã hóa & ẩn tin", font=("Arial Italic", 14)).grid(column=1, row=1)

Label(window, text="1. Nhập văn bản gốc", font=("Arial", 14)).grid(column=0, row=2, sticky=W)
Initialtxt = Entry(window, width=100)
Initialtxt.grid(column=1, row=2, padx=10, pady=5)

Label(window, text="2. Kết quả sau mã hóa RSA (nhị phân)", font=("Arial", 14)).grid(column=0, row=3, sticky=W)
RESULT_ENCODE = Entry(window, width=100)
RESULT_ENCODE.grid(column=1, row=3, padx=10, pady=5)

Label(window, text="3. Kết quả sau giải mã RSA", font=("Arial", 14)).grid(column=0, row=4, sticky=W)
RESULT_DECODE = Entry(window, width=100)
RESULT_DECODE.grid(column=1, row=4, padx=10, pady=5)

status_label = Label(window, text="Chưa thực hiện giấu tin", font=("Arial", 12), fg="gray")
status_label.grid(column=2, row=1, padx=10, pady=5)

Label(window, text="Khóa cá nhân (Private Key)", font=("Arial", 13)).grid(column=0, row=5, sticky=W)
pri_key = Text(window, width=75, height=5)
pri_key.grid(column=1, row=5, padx=10, pady=5)

Label(window, text="Khóa công khai (Public Key)", font=("Arial", 13)).grid(column=0, row=6, sticky=W)
pub_key = Text(window, width=75, height=5)
pub_key.grid(column=1, row=6, padx=10, pady=5)

Button(window, text="🔑 Tạo khóa RSA", width=25, command=create_keys).grid(column=1, row=7, pady=5)
Button(window, text="🔐 Mã hóa bằng RSA", width=25, command=encrypt_text).grid(column=1, row=8, pady=5)
Button(window, text="🔓 Giải mã bằng RSA", width=25, command=decrypt_text).grid(column=1, row=9, pady=5)

Button(window, text="📤 Chọn ảnh (PNG/BMP)", width=35, command=upload_image).grid(column=1, row=10, pady=5)
Button(window, text="📥 Giấu dữ liệu đã mã hóa vào ảnh", width=35, command=embed_data).grid(column=1, row=11, pady=5)
Button(window, text="📤 Trích xuất & giải mã dữ liệu từ ảnh", width=35, command=extract_and_decrypt).grid(column=1, row=12, pady=5)

window.geometry('1300x800')
window.mainloop()
