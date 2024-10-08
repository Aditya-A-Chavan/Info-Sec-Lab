import socket
import json
from client import A51
import base64

def start_server(HOST, PORT):
    server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_s.bind((HOST, PORT))
    server_s.listen(1)
    server_s.settimeout(1.0)  
    print(f"Server listening on IPv4:{PORT}")

    try:
        while True:
            try:
                client_s, addr = server_s.accept()
                print(f"Connected to client at {addr[0]}:{addr[1]}")
                
                client_s.settimeout(5.0)  
                
                try:
                    data = client_s.recv(1024).decode('utf-8')
                    if not data:
                        print("No data received from client.")
                        client_s.close()
                        continue

                    encrypted_message = json.loads(data)
                    encrypted_text = encrypted_message["encrypted_text"]  
                    key = encrypted_message["key"]

                    decoded_encrypted_text = base64.b64decode(encrypted_text)
                    decrypted_text = A51(key).decrypt(decoded_encrypted_text.decode('latin1'))
                    print(f"Encrypted message: {encrypted_text}")
                    print(f"Decrypted Message: {decrypted_text}")

                except json.JSONDecodeError:
                    print("Received invalid JSON data.")

                except KeyError as e:
                    print(f"Missing key in received data: {e}")

                finally:
                    client_s.close()
            
            except socket.timeout:
                continue
            
    except KeyboardInterrupt:
        print("\nServer stopped by user.")

    finally:
        server_s.close()

if __name__ == "__main__":
    start_server('0.0.0.0', 9186)
