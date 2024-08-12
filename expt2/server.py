import socket
import math

def get_key_order(key):
    if key.isdigit():
        num = int(key)
        
        return list(range(num))
    
    
    else:


        order = []
        for i, char in enumerate(key):
            order.append((char, i))
        order.sort()
        return [i for _, i in order]

def decrypt_row_transposition(cipher_text, key):
    key_order = get_key_order(key)
    num_cols = len(key_order)
    num_rows = math.ceil(len(cipher_text) / num_cols)
    
    matrix = [[''] * num_cols for _ in range(num_rows)]
    
    index = 0
    for col in key_order:
        for row in range(num_rows):
            if index < len(cipher_text):
                matrix[row][col] = cipher_text[index]
                index += 1
    
    plain_text = ''
    for row in matrix:
        plain_text += ''.join(row)
    
    return plain_text.strip()

def decrypt_column_transposition(cipher_text, key):
    key_order = get_key_order(key)
    num_rows = len(key_order)
    num_cols = math.ceil(len(cipher_text) / num_rows)
    
    matrix = [''] * num_rows
    
    index = 0
    for row in key_order:
        matrix[row] = cipher_text[index:index+num_cols]
        index += num_cols
    
    plain_text = ''
    for col in range(num_cols):
        for row in range(num_rows):
            if col < len(matrix[row]):
                plain_text += matrix[row][col]
    
    return plain_text.strip()


def start_server(HOST, PORT):
    server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_s.bind((HOST, PORT))
    server_s.listen()

    while True:
        client_s, addr = server_s.accept()

        print(f"Connected to client on: {addr[0]}:{addr[1]}")

        data = client_s.recv(1024).decode('utf-8')
        if not data:
            break

        key, cipher_type, encrypted_text = data.split(',', 2)
        print(f"Received key: {key}")
        print(f"Cipher type: {cipher_type}")
        print(f"Encrypted text: {encrypted_text}")

        if cipher_type == 'row':
            decrypted_text = decrypt_row_transposition(encrypted_text, key)
        elif cipher_type == 'column':
            decrypted_text = decrypt_column_transposition(encrypted_text, key)
        else:
            print("Invalid cipher type received.")
            client_s.close()
            continue

        print(f"Decrypted text: {decrypted_text}")

        client_s.close()

if __name__ == "__main__":    
    HOST = '127.0.0.1'
    PORT = 9196
    start_server(HOST, PORT)