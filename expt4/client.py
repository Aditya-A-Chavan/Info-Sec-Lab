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
    def encrypt(public_key, plaintext):
        e, n = public_key
        m = RSA.string_to_int(plaintext)
        if m >= n:
            raise ValueError("Message is too large for the current key size")
        c = pow(m, e, n)
        return c


def start_comm(server_ip, message, public_key, n, PORT=9186):
    client_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_s.connect((server_ip, PORT))

    encrypted_msg = RSA.encrypt(public_key, message)
    data = {
        'encrypted_text': encrypted_msg,
        'public_key': public_key[0],
        'n': n
    }

    client_s.send(json.dumps(data).encode('utf-8'))
    client_s.close()


if __name__ == "__main__":
    public_key, private_key = RSA.generate_keypair()
    message = input("Enter message: ")
    print(f"Original message: {message}")

    start_comm('127.0.0.1', message, public_key, public_key[1])
