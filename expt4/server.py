import socket
import json
import math
import random
import hashlib

class RSA:
    @staticmethod
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def generate_prime(min_value, max_value):
        prime = random.randint(min_value, max_value)
        while not RSA.is_prime(prime):
            prime = random.randint(min_value, max_value)
        return prime

    @staticmethod
    def mod_inverse(e, phi):
        for d in range(3, phi):
            if (d * e) % phi == 1:
                return d
        return None

    @staticmethod
    def decrypt(private_key, ciphertext):
        d, n = private_key
        return ''.join([chr(pow(char, d, n)) for char in ciphertext])
    
    @staticmethod
    def calculate_phi(n):
        phi = n
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                while n % i == 0:
                    n //= i
                phi *= (1 - 1/i)
        if n > 1:
            phi *= (1 - 1/n)
        return int(phi)

    @staticmethod
    def verify_signature(message, signature, public_key):
        e, n = public_key
        decrypted_signature = pow(signature, e, n)
        hash_object = hashlib.sha256(message.encode())
        message_hash = int(hash_object.hexdigest(), 16) % n
        return decrypted_signature == message_hash

def start_server(HOST, PORT):
    server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_s.bind((HOST, PORT))
    server_s.listen(1)
    server_s.settimeout(1.0)

    print(f"Server listening on {HOST}:{PORT}")

    try:
        while True:
            try:
                client_s, addr = server_s.accept()
                print(f"Connected to client at {addr[0]}:{addr[1]}")
                client_s.settimeout(5.0)

                try:
                    data = client_s.recv(1024).decode('utf-8')
                    if not data:
                        client_s.close()
                        continue

                    message_data = json.loads(data)
                    encrypted_text = message_data['encrypted_text']
                    e = message_data['public_key']
                    n = message_data['n']
                    signature = message_data['signature']

                    phi = RSA.calculate_phi(n)
                    d = RSA.mod_inverse(e, phi)
                    private_key = (d, n)

                    decrypted_msg = RSA.decrypt(private_key, encrypted_text)
                    print(f"Decrypted message: {decrypted_msg}")

                    public_key = (e, n)
                    if RSA.verify_signature(decrypted_msg, signature, public_key):
                        print("Signature verified successfully.")
                    else:
                        print("Signature verification failed.")

                except json.JSONDecodeError:
                    print("Received invalid JSON data.")
                
                except KeyError as e:
                    print(f"Missing key in received data: {e}")
                
                finally:
                    client_s.close()
            except socket.timeout:
                continue
    except KeyboardInterrupt:
        print("\nServer Has Been Stopped by User. Closing session now.")
        server_s.close()

if __name__ == "__main__":
    start_server('0.0.0.0', 9186)