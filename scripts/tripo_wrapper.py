import os
import subprocess

def run_tripo_sr(input_image_path: str, output_dir: str):
    """
    TripoSRの推論処理を呼び出すラッパー関数。
    :param input_image_path: 入力画像（例：front_view.png）
    :param output_dir: 出力ディレクトリ（例：data/output/）
    """

    # TripoSRの作業ディレクトリへ移動
    tripo_sr_dir = "/workspace/tripo_sr"  # Dockerfileでcloneした場所

    # 入出力ファイルの絶対パス取得
    abs_input = os.path.abspath(input_image_path)
    abs_output = os.path.abspath(output_dir)

    os.makedirs(abs_output, exist_ok=True)

    print(f"[TripoSR] Running on image: {abs_input}")
    print(f"[TripoSR] Output directory: {abs_output}")

    command = [
        "python3", "inference.py",
        "--input", abs_input,
        "--output_dir", abs_output,
        "--output_type", "mesh"  # objファイル出力
    ]

    result = subprocess.run(command, cwd=tripo_sr_dir, capture_output=True, text=True)

    if result.returncode != 0:
        print("[TripoSR] Error:")
        print(result.stderr)
        raise RuntimeError("TripoSR inference failed")

    print("[TripoSR] Success")
    print(result.stdout)

    return os.path.join(abs_output, "mesh.obj")
