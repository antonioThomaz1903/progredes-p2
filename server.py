import socket
import threading
import time

clients = {}
lock = threading.Lock()

def handle_client(client_socket, client_address):
    global clients
    client_id = f"@{client_address[1]}"  # Gerar um ID único baseado na porta
    client_socket.send(f"Bem-vindo! Seu ID é {client_id}\n".encode('utf-8'))
    
    with lock:
        if client_id in clients.values():
            client_socket.send("Erro: Nome de usuário já existe.\n".encode('utf-8'))
            client_socket.close()
            return
        clients[client_id] = client_socket
    
    try:
        last_active = time.time()
        while True:
            if time.time() - last_active > 12000:  # Desconectar por inatividade (2 minutos)
                client_socket.send("Desconectado por inatividade.\n".encode('utf-8'))
                break
            client_socket.settimeout(1)  # Checar a cada segundo
            try:
                message = client_socket.recv(1024).decode('utf-8').strip()
                if not message:
                    continue
                last_active = time.time()  # Atualizar tempo de atividade
                broadcast(f"{client_id}: {message}")
            except socket.timeout:
                continue
    except Exception as e:
        print(f"Erro ao lidar com o cliente {client_id}: {e}")
    finally:
        with lock:
            del clients[client_id]
        client_socket.close()

def broadcast(message):
    global clients
    with lock:
        for client_id, client_socket in clients.items():
            try:
                client_socket.send((message + "\n").encode('utf-8'))
            except:
                pass

def start_server(host='127.0.0.1', port=12345):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Servidor rodando em {host}:{port}")

    try:
        while True:
            client_socket, client_address = server.accept()
            print(f"Cliente conectado: {client_address}")
            threading.Thread(target=handle_client, args=(client_socket, client_address)).start()
    except KeyboardInterrupt:
        print("\nEncerrando o servidor.")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()