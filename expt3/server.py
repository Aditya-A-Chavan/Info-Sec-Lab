import socket   
from client import A51


key = 'aditya'


def start_server(HOST, PORT):
    server_s = client_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_s.bind((HOST, PORT))
    server_s.listen(1)

    print(f"Server listening on port {HOST}:{PORT}")

    while True:
        client_s, addr = server_s.accept()

        print(f"Connected to the following machine: {HOST}:{PORT}")

        message = client_s.recv(1024).decode('utf-8')

        

        if not message:
            break


        print(f"message recieved from client: {message}")
        
    



if __name__ == "__main__":
    start_server('10.0.79.143', 9186)