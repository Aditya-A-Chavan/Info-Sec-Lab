def send_data(host='SERVER_IP', port=12345, data='Hello, Server!'):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to the server
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        # Send data to the server
        client_socket.send(data.encode('utf-8'))
        print(f"Sent data: {data}")

        # Receive the acknowledgment from the server
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Server response: {response}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the client socket
        client_socket.close()

if __name__ == "__main__":
    server_ip = input("Enter the server IP address: ")
    message = input("Enter the message to send: ")
