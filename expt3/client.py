import socket
import json



class A51:
    def __init__(self, key):
        self.lfsr1 = self.initialize_lfsr(key, [18, 17, 16, 13], 19)  # Changed taps
        self.lfsr2 = self.initialize_lfsr(key, [21, 20], 22)  # Kept the same
        self.lfsr3 = self.initialize_lfsr(key, [22, 21, 20, 7], 23)  # Changed taps

    def initialize_lfsr(self, key, taps, length):
        lfsr = [0] * length
        for i in range(length):
            lfsr[i] = (ord(key[i % len(key)]) >> (i % 8)) & 1
        return {'state': lfsr, 'taps': taps}

    def shift_lfsr(self, lfsr):
        feedback = 0
        for tap in lfsr['taps']:
            feedback ^= lfsr['state'][tap]  # Changed to use tap directly
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


def start_comm(HOST, message, key, PORT):
    client_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_s.connect((HOST, PORT))
        print(f"connected to server running on machine: {HOST}:{PORT}")

        encrypted_message = json.dumps({
            "encrypted_text": A51(key).encrypt(message),
            "key": key
        })

        client_s.send(encrypted_message.encode('utf-8'))
        print(f"Data that has been sent to server: {encrypted_message}")

    
    except Exception as e:
        print(e)

if __name__ == "__main__":
    server_ip = input("enter server ip: ")
    message = input("enter message to send: ")
    key = input("enter key: ")

    start_comm(server_ip, message, key, PORT=9186)