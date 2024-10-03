import socket
import json
import math
import random

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
    def encrypt(public_key, plaintext):
        e, n = public_key
        cipher = []

          
        for char in plaintext:
            encrypted_char = pow(ord(char), e, n)
            cipher.append(encrypted_char)


        # cipher = [pow(ord(char), e, n) for char in plaintext]
        return cipher

def start_comm(server_ip, message, public_key, PORT=9186):
    client_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_s.connect((server_ip, PORT))

    encrypted_msg = RSA.encrypt(public_key, message)
    data = {
        'encrypted_text': encrypted_msg,
        'public_key': public_key[0],
        'n': public_key[1]
    }
    print("encrypted message:", encrypted_msg)

    client_s.send(json.dumps(data).encode('utf-8'))
    client_s.close()

if __name__ == "__main__":
    public_key, private_key = RSA.generate_keypair()
    message = input("Enter message: ")
    print(f"Original message: {message}")

    start_comm('127.0.0.1', message, public_key)