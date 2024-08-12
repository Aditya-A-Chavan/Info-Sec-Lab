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

def encrypt_row_transposition(message, key):
    key_order = get_key_order(key)
    num_cols = len(key_order)
    num_rows = math.ceil(len(message) / num_cols)
    padded_message = message.ljust(num_rows * num_cols)
    
    matrix = []
    for i in range(num_rows):
        row = padded_message[i * num_cols:(i + 1) * num_cols]
        matrix.append(row)
    
    cipher_text = ""
    for col in key_order:
        for row in range(num_rows):
            cipher_text += matrix[row][col]
    
    return cipher_text

def encrypt_column_transposition(message, key):
    key_order = get_key_order(key)
    num_rows = len(key_order)
    num_cols = math.ceil(len(message) / num_rows)
    padded_message = message.ljust(num_rows * num_cols)
    
    matrix = [''] * num_rows
    for i in range(num_cols):
        for row in range(num_rows):
            index = i * num_rows + row
            if index < len(padded_message):
                matrix[row] += padded_message[index]
    
    cipher_text = ""
    for row in key_order:
        cipher_text += matrix[row]
    
    return cipher_text


def start_comm(HOST, PORT):
    client_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_s.connect((HOST, PORT))

    print(f"Client posting to server on: {HOST}:{PORT}")

    message = input("Enter text you want to encrypt: ")
    key = input("Enter the encryption key: ")
    cipher_type = input("Enter cipher type (row/column): ").lower()

    if cipher_type == 'row':
        encrypted_data = encrypt_row_transposition(message, key)
    elif cipher_type == 'column':
        encrypted_data = encrypt_column_transposition(message, key)
    else:
        print("Invalid cipher type. Please choose 'row' or 'column'.")
        client_s.close()
        exit()

    print(f"Original message: {message}")
    print(f"Encrypted message: {encrypted_data}")

    client_s.send(f"{key},{cipher_type},{encrypted_data}".encode('utf-8'))

    client_s.close()


if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 9196
    start_comm(HOST, PORT)

