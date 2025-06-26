import cv2
import numpy as np
import random

# ---------------- RSA ----------------
def is_prime(n, k=5): 
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_large_prime(bits=512):
    while True:
        p = random.getrandbits(bits)
        if is_prime(p):
            return p

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    m0, x0, x1 = phi, 0, 1
    while e > 1:
        q = e // phi
        e, phi = phi, e % phi
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def generate_keys(bits=512):
    p = generate_large_prime(bits)
    q = generate_large_prime(bits)
    while q == p:  
        q = generate_large_prime(bits)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randrange(2, phi)
    while gcd(e, phi) != 1:  
        e = random.randrange(2, phi)

    d = mod_inverse(e, phi)

    return (e, n), (d, n)

def encrypt_to_binary(message, pub_key):
    e, n = pub_key
    cipher = [pow(ord(char), e, n) for char in message]

    binary = ''
    for c in cipher:
        c_bytes = c.to_bytes((c.bit_length() + 7) // 8, 'big')
        binary += f'{len(c_bytes):08b}'  # 1 byte lưu độ dài
        binary += ''.join(f'{byte:08b}' for byte in c_bytes)

    return binary

def decrypt_from_binary(binary_data, priv_key):
    d, n = priv_key
    i = 0
    cipher = []

    while i < len(binary_data):
        length = int(binary_data[i:i+8], 2)
        i += 8
        byte_str = binary_data[i:i + length * 8]
        i += length * 8

        c_bytes = bytes(int(byte_str[j:j+8], 2) for j in range(0, len(byte_str), 8))
        cipher.append(int.from_bytes(c_bytes, 'big'))

    decrypted_bytes = []
    for c in cipher:
        m = pow(c, d, n)
        if m > 255:
            raise ValueError(f"Giá trị sau giải mã vượt quá 1 byte: {m}")
        decrypted_bytes.append(m)

    return bytes(decrypted_bytes).decode('utf-8')




# ---------------- LSB ----------------
def embed_text_lsb(img_array, binary_data):
    flat = img_array.flatten()

    if len(binary_data) > len(flat):
        raise ValueError("Dữ liệu quá lớn để nhúng vào ảnh.")

    for i in range(len(binary_data)):
        flat[i] = np.uint8((int(flat[i]) & ~1) | int(binary_data[i]))

    return flat.reshape(img_array.shape)

def extract_text_lsb(img_array, n_bits):
    flat = img_array.flatten()
    bits = [str(flat[i] & 1) for i in range(n_bits)]
    return ''.join(bits)


# ---------------- Test ----------------

# plaintext = input("Nhập bản rõ: ")

# public_key, private_key = generate_keys(bits=16)
# print("Khóa công khai:", public_key)
# print("Khóa cá nhân:", private_key)

# binary_cipher = encrypt_to_binary(plaintext, public_key)
# print("Chuỗi nhị phân đã mã hóa:", binary_cipher)


# img = cv2.imread('download.jpg')
# if img is None:
#     raise FileNotFoundError("Không tìm thấy ảnh download.jpg")

# npixels = np.array(img)


# modified_img = embed_text_lsb(npixels.copy(), binary_cipher)
# cv2.imwrite('stego_image.png', modified_img)
# print("Đã giấu tin vào ảnh 'stego_image.png'")


# recovered_binary = extract_text_lsb(modified_img, len(binary_cipher))
# print("Chuỗi nhị phân trích được:", recovered_binary)


# recovered_plaintext = decrypt_from_binary(recovered_binary, private_key)
# print("Văn bản khôi phục từ ảnh:", recovered_plaintext)
