import socket
import random

PASSWORD = "maramag"

def get_rating(guesses):
    if guesses <= 5:
        return "Excellent"
    elif guesses <= 20:
        return "Very Good"
    else:
        return "Good/Fair"

def handle_client(client_socket, secret_number):
    client_socket.send("Welcome, Client!".encode())
    password = client_socket.recv(1024).decode()

    if password != PASSWORD:
        client_socket.send("Incorrect password. Connection closed.".encode())
        client_socket.close()
        return

    client_socket.send("Access granted. Start guessing a number between 1 and 100.".encode())

    guess_count = 0
    while True:
        guess_data = client_socket.recv(1024).decode()
        if not guess_data:
            break
        guess = int(guess_data)
        guess_count += 1

        if guess < secret_number:
            client_socket.send("Too low".encode())
        elif guess > secret_number:
            client_socket.send("Too high".encode())
        else:
            rating = get_rating(guess_count)
            message = f"Correct! Number of guesses: {guess_count}. Rating: {rating}"
            client_socket.send(message.encode())
            break

    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)
    print('Server listening on port 12345...')

    while True:
        client_socket, client_address = server_socket.accept()
        print(f'Accepted connection from {client_address[0]}:{client_address[1]}')
        secret_number = random.randint(1, 100)
        handle_client(client_socket, secret_number)

if __name__ == "__main__":
    start_server()
