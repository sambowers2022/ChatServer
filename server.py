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
        client.send(str.encode(msg))

def handle_client_wrapper(conn, addr):
    handle_client(conn, addr)
    if conn in clients:
        clients.remove(conn)
    conn.close()
    broadcast(f"{addr} has disconnected")

def handle_client(conn, addr):
    print('Connected by', addr)
    while True:
        data = conn.recv(1024)
        if not data:
            break
        opts = data.decode("utf-8").split(",")
        code = auth.login(db, opts) 
        conn.send(code.to_bytes(3))
        if code == 200 or code == 201:
            print((conn, addr))
            clients.append(conn)
            broadcast(f"{opts[1]} has joined the chat")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                broadcast(opts[1] + " > " + data.decode("utf-8"), conn)
        else:
            conn.close()
            break

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        while True:
            s.listen()
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client_wrapper, args=(conn, addr))
            client_thread.start()

except KeyboardInterrupt:
    print("Server shutting down")
    for client in clients:
        client.close()
    s.close()
    print("Server shut down")
    exit(0)

