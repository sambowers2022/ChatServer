import socket
import auth
import db
import threading

HOST = '127.0.0.1'
PORT = 65432

db = db.init()

clients = []

def broadcast(msg, sender=None):
    for client in clients:
        if client == sender:
            continue
        client[0].send(msg.encode("utf-8"))

def handle_client(conn, addr):
    print('Connected by', addr)
    while True:
        data = conn.recv(1024)
        if not data:
            break
        code = auth.login(db, data.decode("utf-8").split(","))
        conn.send(code.to_bytes(3))
        if code == 200 or code == 201:
            print((conn, addr))
            clients.append((conn, addr))
            broadcast(f"{addr} has joined the chat")
            while True:
                data = conn.recv(1024)
                broadcast(data.decode("utf-8"), (conn, addr))
        else:
            conn.close()
            break

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        while True:
            s.listen()
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()
except KeyboardInterrupt:
    print("Server shutting down")
    for client in clients:
        client[0].close()
    s.close()
    exit(0)

