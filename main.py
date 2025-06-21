# from tkinter import *
# from tkinter import filedialog
# from PIL import Image, ImageTk

# # Import các hàm xử lý ở file riêng (chưa định nghĩa)


# # === GIAO DIỆN CHÍNH ===
# window = Tk()
# window.title("Ứng dụng giấu tin trong ảnh bằng LSB kết hợp mã hóa RSA")

# selected_image = None
# preview_label = None

# def upload_image():
#     global selected_image, preview_label
#     filepath = filedialog.askopenfilename(title="Chọn ảnh để giấu tin", filetypes=[("Image files", "*.png *.bmp")])
#     if filepath:
#         selected_image = filepath
#         img = Image.open(filepath)
#         img.thumbnail((300, 300))
#         img_tk = ImageTk.PhotoImage(img)
#         if preview_label:
#             preview_label.config(image=img_tk)
#             preview_label.image = img_tk
#         else:
#             preview_label = Label(window, image=img_tk)
#             preview_label.image = img_tk
#             preview_label.grid(column=2, row=2, rowspan=10, padx=20, pady=10)

# Label(window, text="🔐 RSA + 🖼️ LSB Steganography", font=("Arial Bold", 22), fg="blue").grid(column=1, row=0, pady=10)
# Label(window, text="Giấu tin an toàn bằng kỹ thuật mã hóa & ẩn tin", font=("Arial Italic", 14)).grid(column=1, row=1)

# # === BƯỚC 1: NHẬP & MÃ HÓA ===
# Label(window, text="1. Nhập văn bản gốc", font=("Arial", 14)).grid(column=0, row=2, sticky=W)
# Initialtxt = Entry(window, width=100)
# Initialtxt.grid(column=1, row=2, padx=10, pady=5)

# Label(window, text="2. Kết quả sau mã hóa RSA (base64)", font=("Arial", 14)).grid(column=0, row=3, sticky=W)
# RESULT_ENCODE = Entry(window, width=100)
# RESULT_ENCODE.grid(column=1, row=3, padx=10, pady=5)

# Label(window, text="3. Kết quả sau giải mã RSA", font=("Arial", 14)).grid(column=0, row=4, sticky=W)
# RESULT_DECODE = Entry(window, width=100)
# RESULT_DECODE.grid(column=1, row=4, padx=10, pady=5)

# # === BƯỚC 2: KHÓA RSA ===
# Label(window, text="Khóa cá nhân (Private Key)", font=("Arial", 13)).grid(column=0, row=5, sticky=W)
# pri_key = Text(window, width=75, height=5)
# pri_key.grid(column=1, row=5, padx=10, pady=5)

# Label(window, text="Khóa công khai (Public Key)", font=("Arial", 13)).grid(column=0, row=6, sticky=W)
# pub_key = Text(window, width=75, height=5)
# pub_key.grid(column=1, row=6, padx=10, pady=5)

# # === BƯỚC 3: CÁC NÚT CHỨC NĂNG ===
# Button(window, text="🔑 Tạo khóa RSA", width=25, command="").grid(column=1, row=7, pady=5)
# Button(window, text="🔐 Mã hóa bằng RSA", width=25, command="").grid(column=1, row=8, pady=5)
# Button(window, text="🔓 Giải mã bằng RSA", width=25, command="").grid(column=1, row=9, pady=5)

# # === BƯỚC 4: LSB ===
# Button(window, text="📤 Chọn ảnh (PNG/BMP)", width=35, command=upload_image).grid(column=1, row=10, pady=5)
# Button(window, text="📥 Giấu dữ liệu đã mã hóa vào ảnh", width=35, command="").grid(column=1, row=11, pady=5)
# Button(window, text="📤 Trích xuất & giải mã dữ liệu từ ảnh", width=35, command="").grid(column=1, row=12, pady=5)

# window.geometry('1300x750')
# window.mainloop()