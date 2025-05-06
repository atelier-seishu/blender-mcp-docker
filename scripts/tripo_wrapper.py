import os
import subprocess

def run_tripo_sr(image_path: str, output_dir: str):
    print(f"[TripoSR] Running on image: {image_path}")
    print(f"[TripoSR] Output directory: {output_dir}")

    # 出力先ディレクトリ（run.pyが使う内部的な0番ディレクトリ）を事前に作成
    target_mesh_dir = os.path.join(output_dir, "0")
    os.makedirs(target_mesh_dir, exist_ok=True)

    result = subprocess.run([
        "python", "tripo_sr/run.py",
        image_path,
        "--output-dir", output_dir,
        "--device", "cpu",
        "--model-save-format", "obj",
        "--no-remove-bg"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        print("[TripoSR] Error:")
        print(result.stderr.decode())
        raise RuntimeError("TripoSR inference failed")

    # mesh.obj の存在確認
    mesh_path = os.path.join(target_mesh_dir, "mesh.obj")
    if os.path.isfile(mesh_path):
        print(f"[TripoSR] Found mesh at: {mesh_path}")
        return mesh_path
    else:
        raise FileNotFoundError(f"mesh.obj not found at expected location: {mesh_path}")
