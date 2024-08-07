import socket

def start_comm(HOST, message, PORT):
    client_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_s.connect((HOST, PORT))
        print(f"connected to server running machine: {HOST}:{PORT}")

        client_s.send(message.encode('utf-8'))
        print(f"Data that has been sent to server: {message}")

        response = client_s.recv(1024).decode('utf-8')

        print(f"response from server: {response}")
    
    except Exception as e:
        print(e)

if __name__ == "__main__":
    server_ip = input("enter server ip: ")
    message = input("enter message to send: ")

    start_comm(server_ip, message, PORT=9186)