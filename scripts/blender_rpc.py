import socket

def send_to_blender(obj_path):
    s = socket.socket()
    s.connect(("host.docker.internal", 9999))  # Docker → ホスト接続用アドレス
    s.send(obj_path.encode())
    response = s.recv(1024)
    print("Blender response:", response.decode())
    s.close()
