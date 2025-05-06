from fastapi import FastAPI
from pydantic import BaseModel
import subprocess

app = FastAPI()

class MeshRequest(BaseModel):
    input_mesh: str
    output_dir: str

@app.post("/process")
def process_mesh(req: MeshRequest):
    print(f"[INFO] Received mesh for processing: {req.input_mesh}")
    try:
        result = subprocess.run([
            "/usr/bin/blender",           # Docker外にBlenderがある場合は '/usr/bin/blender' にする必要なし
            "--background",
            "--python", "blender_mcp/main.py",
            "--", req.input_mesh, req.output_dir
        ], check=True, capture_output=True, text=True)
        print(result.stdout)
        return {"success": True}
    except subprocess.CalledProcessError as e:
        print("[ERROR] BlenderMCP failed:", e.stderr)
        return {"success": False, "error": str(e)}
