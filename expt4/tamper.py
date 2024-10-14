import socket
import json

def tamper_message(original_data):

    data = json.loads(original_data)

    if 'encrypted_text' in data:
        tampered_cipher = data['encrypted_text']
        tampered_cipher[0] = tampered_cipher[0] + 1
        data['encrypted_text'] = tampered_cipher

    return json.dumps(data)


def start_proxy(proxy_host, proxy_port, server_host, server_port):
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind((proxy_host, proxy_port))
    proxy_socket.listen(1)

    print(f"Proxy listening on {proxy_host}:{proxy_port}")

    try:
        while True:
            client_conn, client_addr = proxy_socket.accept()
            print(f"Connected to client at {client_addr}")

            try:
                data_from_client = client_conn.recv(1024).decode('utf-8')
                if not data_from_client:
                    client_conn.close()
                    continue

                print("Received data from client:", data_from_client)

                tampered_data = tamper_message(data_from_client)

                print("Tampered data:", tampered_data)

                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_socket.connect((server_host, server_port))
                server_socket.sendall(tampered_data.encode('utf-8'))

                server_response = server_socket.recv(1024).decode('utf-8')
                client_conn.sendall(server_response.encode('utf-8'))

                server_socket.close()

            finally:
                client_conn.close()

    except KeyboardInterrupt:
        print("\nProxy stopped by user.")
    finally:
        proxy_socket.close()
        print("Proxy socket closed.")


if __name__ == "__main__":
    proxy_host = '0.0.0.0'
    proxy_port = 9191

    server_host = '127.0.0.1'
    server_port = 9186

    start_proxy(proxy_host, proxy_port, server_host, server_port)