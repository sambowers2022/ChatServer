import socket
import auth
import db

HOST = '127.0.0.1'
PORT = 65432

db = db.init()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    while True:
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                code = auth.login(db, data.decode("utf-8").split(","))
                conn.send(code.to_bytes(3))


