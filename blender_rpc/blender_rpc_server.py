import bpy
import socket
import threading
import argparse
import os

def load_obj(filepath):
    if not os.path.isfile(filepath):
        print(f"[ERROR] File not found: {filepath}")
        return
    bpy.ops.import_scene.obj(filepath=filepath)
    print(f"[INFO] Successfully imported: {filepath}")

def handle_connection(conn, addr):
    print(f"[INFO] Connected by {addr}")
    try:
        while True:
            data = conn.recv(4096).decode().strip()
            if data:
                print(f"[INFO] Received: {data}")
                load_obj(data)
                conn.sendall(b"Imported\n")
            else:
                break
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()
        print(f"[INFO] Connection closed: {addr}")

def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"[INFO] Blender RPC server listening on port {port}...")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_connection, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=9876, help='Port to listen on (default: 9876)')
    args = parser.parse_args()
    start_server(args.port)
