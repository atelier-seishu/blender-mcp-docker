import socket
import json
import os

# Dockerコンテナ内のパスを、ホスト（Windows）側のパスに変換する
def convert_to_host_path(docker_path: str) -> str:
    docker_root = "/workspace"
    host_root = "C:/project/blender-mcp-docker"  # プロジェクトのローカルパスに合わせて変更
    rel_path = os.path.relpath(docker_path, docker_root)
    return os.path.join(host_root, rel_path).replace("\\", "/")

def call_blender_mcp(mesh_path: str, output_dir: str):
    print(f"[INFO] Sending mesh to BlenderMCP: {mesh_path}")

    # Docker → Windowsパスに変換
    host_mesh_path = convert_to_host_path(mesh_path)
    host_output_dir = convert_to_host_path(output_dir)

    payload = {
        "type": "execute_code",
        "params": {
            "code": f'''
import bpy
import os

# 既存オブジェクト削除
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# OBJファイルの読み込み
bpy.ops.import_scene.obj(filepath="{host_mesh_path}")

# 出力ファイルパス
output_path = os.path.join("{host_output_dir}", os.path.basename("{host_mesh_path}").replace(".obj", "_processed.glb"))

# GLB形式でエクスポート
bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
'''
        }
    }

    try:
        with socket.create_connection(("host.docker.internal", 9876), timeout=10) as sock:
            sock.sendall(json.dumps(payload).encode('utf-8'))

            response = b''
            while True:
                data = sock.recv(4096)
                if not data:
                    break
                response += data

            result = json.loads(response.decode('utf-8'))

            if result.get("status") != "success":
                raise RuntimeError(f"[ERROR] BlenderMCP error: {result.get('message')}")
            print("[INFO] BlenderMCP execution succeeded")

    except Exception as e:
        print("[ERROR] BlenderMCP call failed during socket communication.")
        raise RuntimeError("Failed to connect to BlenderMCP via socket") from e
