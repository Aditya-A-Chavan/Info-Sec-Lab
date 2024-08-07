import socket


class encryption():
    def affine_encrypt(self, text: str, a: int, b: int) -> str:
        encrypted_text = ""
        for char in text:
            if char.isalpha():
                if char.isupper():
                    encrypted_text += chr((a * (ord(char) - ord('A')) + b) % 26 + ord('A'))
                else:
                    encrypted_text += chr((a * (ord(char) - ord('a')) + b) % 26 + ord('a'))
            else:
                encrypted_text += char
        return encrypted_text


HOST = '127.0.0.1'
PORT = 9196

client_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_s.connect((HOST, PORT))


print(f"Client posting to server on: {HOST}:{PORT}")

message = input("Enter text you want to encrypt: ")


data = encryption().affine_encrypt(message, 5, 8)

client_s.send(data.encode('utf-8'))


client_s.close()
