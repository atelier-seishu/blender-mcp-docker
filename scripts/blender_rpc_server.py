import bpy
import socket
import json
import threading
from bpy.app.handlers import persistent

PORT = 9876

def handle_connection(conn):
    try:
        data = conn.recv(4096)
        request = json.loads(data.decode("utf-8"))
        code = request.get("params", {}).get("code", "")
        exec(code, {"bpy": bpy})
        response = {"status": "success"}
    except Exception as e:
        response = {"status": "error", "message": str(e)}
    conn.sendall(json.dumps(response).encode("utf-8"))
    conn.close()

def start_rpc_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", PORT))
    server.listen(1)
    print(f"[INFO] Blender RPC Server started at {PORT}")

    def accept_loop():
        while True:
            conn, _ = server.accept()
            threading.Thread(target=handle_connection, args=(conn,), daemon=True).start()

    threading.Thread(target=accept_loop, daemon=True).start()

@persistent
def load_post_handler(dummy):
    # Blender起動完了後にRPCサーバーを開始し、終了防止タイマーを設定
    start_rpc_server()

    def keep_alive():
        return 1.0  # 1秒ごとにタイマー継続

    bpy.app.timers.register(keep_alive, first_interval=1.0)

# ハンドラ登録
bpy.app.handlers.load_post.append(load_post_handler)
