import socket
import json
import base64



class A51:
    def __init__(self, key):
        self.lfsr1 = self.initialize_lfsr(key, [18, 17, 16, 13], 19)
        self.lfsr2 = self.initialize_lfsr(key, [21, 20], 22)
        self.lfsr3 = self.initialize_lfsr(key, [22, 21, 20, 7], 23)
    def initialize_lfsr(self, key, taps, length):
        lfsr = [0] * length
        for i in range(length):
            lfsr[i] = (ord(key[i % len(key)]) >> (i % 8)) & 1
        return {'state': lfsr, 'taps': taps}

    def shift_lfsr(self, lfsr):
        feedback = 0
        for tap in lfsr['taps']:
            feedback ^= lfsr['state'][tap]  
        lfsr['state'] = [feedback] + lfsr['state'][:-1]
        return lfsr['state'][-1]

    def majority(self, bit1, bit2, bit3):
        return (bit1 & bit2) | (bit2 & bit3) | (bit3 & bit1)

    def generate_keystream(self, length):
        keystream = []
        for _ in range(length):
            majority_bit = self.majority(self.lfsr1['state'][8], self.lfsr2['state'][10], self.lfsr3['state'][10])
            if self.lfsr1['state'][8] == majority_bit:
                self.shift_lfsr(self.lfsr1)
            if self.lfsr2['state'][10] == majority_bit:
                self.shift_lfsr(self.lfsr2)
            if self.lfsr3['state'][10] == majority_bit:
                self.shift_lfsr(self.lfsr3)
            keystream_bit = self.lfsr1['state'][-1] ^ self.lfsr2['state'][-1] ^ self.lfsr3['state'][-1]
            keystream.append(keystream_bit)
        return keystream

    def encrypt(self, plaintext):
        keystream = self.generate_keystream(len(plaintext) * 8)
        plaintext_bits = self.text_to_bits(plaintext)
        ciphertext_bits = [plaintext_bits[i] ^ keystream[i] for i in range(len(plaintext_bits))]
        return self.bits_to_text(ciphertext_bits)

    def decrypt(self, ciphertext):
        return self.encrypt(ciphertext)

    def text_to_bits(self, text):
        return [int(bit) for char in text for bit in format(ord(char), '08b')]

    def bits_to_text(self, bits):
        chars = [chr(int(''.join(str(bit) for bit in bits[i:i+8]), 2)) for i in range(0, len(bits), 8)]
        return ''.join(chars)


def start_comm(server_ip, message, key, PORT=9186):
    client_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_s.connect((server_ip, PORT))

    cipher = A51(key)
    encrypted_text = cipher.encrypt(message)

    base64_encrypted_text = base64.b64encode(encrypted_text.encode('latin1')).decode('utf-8')
    
    data_to_send = json.dumps({
        "encrypted_text": base64_encrypted_text,
        "key": key
    })

    client_s.send(data_to_send.encode('utf-8'))
    print(f"Data that has been sent to server: {data_to_send}")

    client_s.close()

if __name__ == "__main__":
    server_ip = input("enter server ip: ")
    message = input("enter message to send: ")
    key = input("enter key: ")

    start_comm(server_ip, message, key, PORT=9186)