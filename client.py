import socket
import threading

def receive_messages(sock):
    try:
        while True:
            message = sock.recv(1024).decode('utf-8').strip()
            if not message:
                break
            print(message)
    except:
        print("Conexão perdida com o servidor.")
    finally:
        sock.close()

def start_client(host='127.0.0.1', port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        threading.Thread(target=receive_messages, args=(client_socket,)).start()

        while True:
            message = input()
            if message.lower() == '/exit':
                break
            client_socket.send((message + "\n").encode('utf-8'))
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()