import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

prompt = client_socket.recv(1024).decode()
print(prompt)
password = input("Password: ")
client_socket.send(password.encode())

response = client_socket.recv(1024).decode()
print(response)

if "Access granted" not in response:
    client_socket.close()
    exit()

while True:
    guess = input("Enter your guess (1-100): ")
    client_socket.send(guess.encode())
    feedback = client_socket.recv(1024).decode()
    print("Server:", feedback)
    if "Correct!" in feedback:
        break

client_socket.close()