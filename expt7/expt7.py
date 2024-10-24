import random
import time

class AuthenticationServer:
    def __init__(self):
        self.password = "secret123"
        
    def generate_challenge(self):
        return random.randint(100, 999)
    
    def verify_response(self, ra, rb, client_response):
        expected_response = ra % rb
        return client_response == expected_response
    
    def authenticate_client(self, client):
        print("\nStarting Authentication Process...")
        print("-----------------------------------")
        
        rb = self.generate_challenge()
        print(f"Server (Bob) generated challenge Rb: {rb}")
        
        ra = client.send_initial_message()
        print(f"Server received Ra from client: {ra}")
        
        client_response = client.receive_challenge(rb)
        print(f"Server received response from client: {client_response}")
        
        server_calculation = ra % rb
        print(f"Server calculated Ra mod Rb: {server_calculation}")
        
        if self.verify_response(ra, rb, client_response):
            print("\n✅ Authentication Successful! Client verified.")
            return True
        else:
            print("\n❌ Authentication Failed! Invalid response.")
            return False

class AuthenticationClient:
    def __init__(self, password):
        self.password = password
        self.ra = None
        
    def generate_ra(self):
        self.ra = random.randint(100, 999)
        return self.ra
    
    def send_initial_message(self):
        self.ra = self.generate_ra()
        return self.ra
    
    def receive_challenge(self, rb):
        response = self.ra % rb
        return response

def simulate_authentication(client_password):
    server = AuthenticationServer()
    client = AuthenticationClient(client_password)
    
    time.sleep(1)
    result = server.authenticate_client(client)
    
    return result

if __name__ == "__main__":
    print("Challenge-Response Authentication Protocol Simulation")
    print("==================================================")
    
    print("\nTest 1: Correct Password")
    simulate_authentication("secret123")
    
    time.sleep(1)
    print("\nTest 2: Simulating potential malicious attempt")
    
    class MaliciousClient:
        def send_initial_message(self):
            return random.randint(100, 999)
        def receive_challenge(self, rb):
            return random.randint(0, rb-1)
            
    server = AuthenticationServer()
    server.authenticate_client(MaliciousClient())