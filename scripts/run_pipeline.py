import os
import glob
import shutil
import logging
from pathlib import Path

from scripts.tripo_wrapper import run_tripo_sr
from scripts.blender_rpc import call_blender_mcp

# ディレクトリ構成
INPUT_DIR = "data/input"
OUTPUT_DIR = "data/output"
TMP_DIR = "data/tmp"

# ログ設定
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def generate_mesh(input_image_path, output_mesh_path):
    logging.info(f"[INFO] Generating mesh from image: {input_image_path}")
    os.makedirs(os.path.dirname(output_mesh_path), exist_ok=True)

    mesh_path = run_tripo_sr(input_image_path, os.path.dirname(output_mesh_path))
    if not mesh_path or not os.path.exists(mesh_path):
        raise FileNotFoundError(f"[ERROR] Mesh was not generated: {mesh_path}")

    if mesh_path != output_mesh_path:
        shutil.move(mesh_path, output_mesh_path)

    logging.info(f"[INFO] Mesh saved to: {output_mesh_path}")
    return output_mesh_path

def process_all_images():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(TMP_DIR, exist_ok=True)

    image_files = glob.glob(os.path.join(INPUT_DIR, "*.png")) + glob.glob(os.path.join(INPUT_DIR, "*.jpg"))
    if not image_files:
        logging.warning("[WARN] No input images found.")
        return

    for image_path in image_files:
        stem = Path(image_path).stem
        mesh_path = os.path.join(TMP_DIR, f"{stem}_mesh.obj")
        try:
            mesh_path = generate_mesh(image_path, mesh_path)
            call_blender_mcp(mesh_path, OUTPUT_DIR)
        except Exception as e:
            logging.error(f"[ERROR] Error processing {image_path}: {e}")
        else:
            # 正常に完了した場合のみ .obj を削除
            if os.path.exists(mesh_path):
                os.remove(mesh_path)

if __name__ == "__main__":
    process_all_images()
