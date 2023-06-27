import socket

def send_messages():
    host = 'localhost'
    # port = 65432
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(b'Hello, World!')
        data = s.recv(1024)

    print('Received:', repr(data))

if __name__ == "__main__":
    send_messages()
