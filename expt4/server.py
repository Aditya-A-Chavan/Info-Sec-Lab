import socket
import json
import math
import random


class RSA:
    @staticmethod
    def is_prime(n):
        if n < 2:
            return False
        i = 2
        while i <= int(math.sqrt(n)):
            if n % i == 0:
                return False
            i += 1
        return True

    @staticmethod
    def generate_prime(min_value, max_value):
        prime = random.randint(min_value, max_value)
        while not RSA.is_prime(prime):
            prime = random.randint(min_value, max_value)
        return prime

    @staticmethod
    def mod_inverse(e, phi):
        d = 3
        while d < phi:
            if (d * e) % phi == 1:
                return d
            d += 1
        return None

    @staticmethod
    def generate_keypair():
        p = RSA.generate_prime(1000, 10000)
        q = RSA.generate_prime(1000, 10000)
        n = p * q
        phi = (p - 1) * (q - 1)
        
        e = random.randrange(1, phi)
        g = math.gcd(e, phi)
        while g != 1:
            e = random.randrange(1, phi)
            g = math.gcd(e, phi)
        
        d = RSA.mod_inverse(e, phi)
        return ((e, n), (d, n))

    @staticmethod
    def string_to_int(message):
        result = ""
        i = 0
        while i < len(message):
            char = message[i]
            result += str(ord(char))
            i += 1
        return int(result)

    @staticmethod
    def int_to_string(number):
        string = str(number)
        result = ""
        i = 0
        while i < len(string):
            char_code = int(string[i:i+2])
            result += chr(char_code)
            i += 2
        return result

    @staticmethod
    def decrypt(private_key, ciphertext):
        d, n = private_key
        m = pow(ciphertext, d, n)
        return RSA.int_to_string(m)


def start_server(HOST, PORT):
    server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_s.bind((HOST, PORT))
    server_s.listen(1)
    server_s.settimeout(1.0)

    print(f"Server listening on IPv4:{PORT}")

    private_key = None

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

                    encrypted_message = json.loads(data)
                    encrypted_text = encrypted_message['encrypted_text']
                    e = encrypted_message['public_key']
                    n = encrypted_message['n']

                    if private_key is None:
                        _, private_key = RSA.generate_keypair()

                    decrypted_msg = RSA.decrypt(private_key, encrypted_text)
                    print(f"Decrypted message: {decrypted_msg}")

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
