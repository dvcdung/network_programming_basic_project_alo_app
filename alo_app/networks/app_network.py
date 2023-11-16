import socket


class Net():
    SERVER_IP = "127.0.0.1"
    SERVER_PORT = 12345
    client_socket = None

    def connect_to_server(self):
        if not self.client_socket:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.SERVER_IP, self.SERVER_PORT))

    def disconnect_to_server(self):
        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None
        
    def send_to_server(self, id, data):
        if self.client_socket:
            self.client_socket.send(f"{id}:{data}".encode())

    def receive_from_server(self):
        if self.client_socket:
            response = self.client_socket.recv(2048).decode()
            return response.split(":", 1)