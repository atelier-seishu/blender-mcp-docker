import os
import requests

def call_blender_mcp(mesh_path: str, output_dir: str):
    print(f"[INFO] Sending mesh to BlenderMCP: {mesh_path}")
    url = "http://localhost:9876/process"
    payload = {
        "input_mesh": mesh_path,
        "output_dir": output_dir
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("[ERROR] BlenderMCP call failed")
        print(e)
        raise

    result = response.json()
    if not result.get("success", False):
        raise RuntimeError(f"BlenderMCP failed: {result}")
    print("[INFO] BlenderMCP call succeeded")
