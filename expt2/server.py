import socket

class decrypton():
    def affine_decrypt(self, encrypted_text, a: int, b: int):
        decrypted_text = ""
        a_inverse = self.mod_inverse(a, 26)
        for char in encrypted_text:
            if char.isalpha():
                if char.isupper():
                    decrypted_text += chr((a_inverse * (ord(char) - ord('A') - b)) % 26 + ord('A'))
                else:
                    decrypted_text += chr((a_inverse * (ord(char) - ord('a') - b)) % 26 + ord('a'))
            else:
                decrypted_text += char
        return decrypted_text

    def mod_inverse(self, a: int, m: int) -> int:
        for i in range(1, m):
            if (a * i) % m == 1:
                return i
        return None

HOST = '127.0.0.1'
PORT = 9196

server_s = client_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_s.bind((HOST, PORT))
server_s.listen()

while True:
    client_s, addr = server_s.accept()

    print(f"Connected to client on: {HOST}:{PORT}")

    encrypted_text = client_s.recv(1024).decode('utf-8')
    print(f"Encrypted text rec from client: {encrypted_text}")
    if not encrypted_text:
        break

    print("Decrypted on server: ", decrypton().affine_decrypt(encrypted_text, 5, 8))

    # server_s.close()

