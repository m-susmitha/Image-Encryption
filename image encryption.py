from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from PIL import Image
import io

def encrypt_image(image_path, key):
    # Load image
    with open(image_path, 'rb') as img_file:
        image_bytes = img_file.read()

    # Pad the image bytes
    padded_data = pad(image_bytes, AES.block_size)

    # Generate a random initialization vector (IV)
    iv = get_random_bytes(AES.block_size)

    # Create AES cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Encrypt the image data
    encrypted_data = cipher.encrypt(padded_data)

    # Save encrypted image
    encrypted_image_path = "encrypted_image.png"
    with open(encrypted_image_path, 'wb') as encrypted_file:
        encrypted_file.write(iv + encrypted_data)

    print("Image encrypted and saved as", encrypted_image_path)

def decrypt_image(encrypted_image_path, key):
    # Load encrypted image
    with open(encrypted_image_path, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()

    # Extract IV
    iv = encrypted_data[:AES.block_size]
    encrypted_data = encrypted_data[AES.block_size:]

    # Create AES cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt the image data
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

    # Display the decrypted image
    decrypted_image = Image.open(io.BytesIO(decrypted_data))
    decrypted_image.show()

# Example usage
key = get_random_bytes(16)  # 128-bit key for AES
image_path = "your_image.png"  # Replace with the path to your image

# Encrypt image
encrypt_image(image_path, key)

# Decrypt image
decrypt_image("encrypted_image.png", key)
