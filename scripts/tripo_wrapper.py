import os
import subprocess

def run_tripo_sr(image_path: str, output_dir: str):
    """
    指定された画像に対してTripoSRを実行し、メッシュをoutput_dirに出力する。
    """
    print(f"[TripoSR] Running on image: {image_path}")
    print(f"[TripoSR] Output directory: {output_dir}")

    result = subprocess.run([
        "python", "tripo_sr/run.py",
        image_path,
        "--output-dir", output_dir,
        "--device", "cpu",  # GPU使うなら "cuda:0" にする
        "--model-save-format", "obj",
        "--no-remove-bg"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        print("[TripoSR] Error:")
        print(result.stderr.decode())
        raise RuntimeError("TripoSR inference failed")
