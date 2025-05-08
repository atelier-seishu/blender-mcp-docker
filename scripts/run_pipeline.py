import os
import shutil
import logging
import subprocess

from scripts.tripo_wrapper import run_tripo_sr
from scripts.blender_rpc import call_blender_mcp
from scripts.merge_views import merge_three_views

INPUT_DIR = "data/input"
OUTPUT_DIR = "data/output"
TMP_DIR = "data/tmp"
MERGED_IMAGE_PATH = os.path.join(TMP_DIR, "merged_input.jpg")
MERGED_MESH_PATH = os.path.join(TMP_DIR, "merged_input_mesh.obj")
LOWPOLY_SCRIPT = "scripts/lowpoly_blender_postprocess.py"

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

def simplify_mesh(obj_path):
    logging.info(f"[INFO] Simplifying mesh via Blender: {obj_path}")
    try:
        subprocess.run([
            "blender", "--background", "--python", LOWPOLY_SCRIPT, "--", obj_path
        ], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"[ERROR] Blender simplification failed: {e}")
        raise

def process_merged_views():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(TMP_DIR, exist_ok=True)

    try:
        merged_image_path = merge_three_views()
        merged_mesh_path = generate_mesh(merged_image_path, MERGED_MESH_PATH)

        simplify_mesh(merged_mesh_path)  # ← 追加！

        call_blender_mcp({"merged": merged_mesh_path}, OUTPUT_DIR)

    except Exception as e:
        logging.error(f"[ERROR] Failed to process merged 3-view images: {e}")

if __name__ == "__main__":
    process_merged_views()
