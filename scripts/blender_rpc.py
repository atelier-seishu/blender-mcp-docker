import os
import requests

def call_blender_mcp(mesh_path: str, output_dir: str):
    """
    Docker内からDocker外のBlenderMCP（ホスト側）へRPCリクエストを送信して処理を実行する。
    Blender側は port 9876 で待機している前提。
    """
    url = "http://host.docker.internal:9876/process"
    payload = {
        "input_mesh": mesh_path,
        "output_dir": output_dir
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("[ERROR] Failed to contact BlenderMCP")
        print(e)
        raise RuntimeError("BlenderMCP RPC call failed") from e

    result = response.json()
    if not result.get("success", False):
        raise RuntimeError(f"BlenderMCP returned failure: {result}")
    else:
        print("[INFO] BlenderMCP execution completed successfully")
