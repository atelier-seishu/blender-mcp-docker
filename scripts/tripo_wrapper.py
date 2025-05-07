import os
import subprocess

def run_tripo_sr(image_path: str, output_dir: str) -> str:
    print(f"[TripoSR] Running on image: {image_path}")
    print(f"[TripoSR] Output directory: {output_dir}")

    # 正しい引数でTripoSRを実行（--input → 位置引数）
    command = [
        "python", "tripo_sr/run.py",
        image_path,  # 位置引数として画像パス
        "--output-dir", output_dir
    ]

    # subprocessでTripoSRを実行
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        print("[TripoSR] Error occurred during execution:")
        print(result.stderr)
        return None

    mesh_path = os.path.join(output_dir, "0", "mesh.obj")
    if not os.path.exists(mesh_path):
        print(f"[TripoSR] Mesh not found at expected location: {mesh_path}")
        return None

    print(f"[TripoSR] Found mesh at: {mesh_path}")
    return mesh_path
