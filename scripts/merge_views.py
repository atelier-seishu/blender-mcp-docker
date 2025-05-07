import os
import glob
from PIL import Image

INPUT_ROOT = "data/input"
OUTPUT_PATH = "data/tmp/merged_input.jpg"
VIEW_ORDER = ["front", "side", "back"]  # 並び順の制御

def find_image_in_dir(dir_path):
    for ext in ("*.jpg", "*.jpeg", "*.png"):
        files = glob.glob(os.path.join(dir_path, ext))
        if files:
            return files[0]
    return None

def merge_three_views():
    print("[INFO] Merging views from:", VIEW_ORDER)
    images = []

    for view in VIEW_ORDER:
        view_dir = os.path.join(INPUT_ROOT, view)
        if not os.path.isdir(view_dir):
            raise FileNotFoundError(f"[ERROR] Missing directory: {view_dir}")

        image_path = find_image_in_dir(view_dir)
        if not image_path:
            raise FileNotFoundError(f"[ERROR] No image found in {view_dir}")

        img = Image.open(image_path).convert("RGB")
        images.append(img)

    # 高さを揃えて横並びで統合
    heights = [img.height for img in images]
    max_height = max(heights)
    resized = [img.resize((int(img.width * max_height / img.height), max_height)) for img in images]
    total_width = sum(img.width for img in resized)

    merged = Image.new("RGB", (total_width, max_height))
    x_offset = 0
    for img in resized:
        merged.paste(img, (x_offset, 0))
        x_offset += img.width

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    merged.save(OUTPUT_PATH)
    print(f"[INFO] Merged image saved to: {OUTPUT_PATH}")
    return OUTPUT_PATH

if __name__ == "__main__":
    merge_three_views()
