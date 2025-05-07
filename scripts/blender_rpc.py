import socket
import json
import os

# Dockerコンテナ内のパスを、ホスト（Windows）側のパスに変換する
def convert_to_host_path(docker_path: str) -> str:
    docker_root = "/workspace"
    host_root = "C:/project/blender-mcp-docker"  # プロジェクトのローカルパスに合わせて変更
    rel_path = os.path.relpath(docker_path, docker_root)
    return os.path.join(host_root, rel_path).replace("\\", "/")


def call_blender_mcp(mesh_paths: dict, output_dir: str):
    print(f"[INFO] Sending merged mesh to BlenderMCP...")

    host_output_dir = convert_to_host_path(output_dir)
    host_input_dir = convert_to_host_path("data/input")

    # 1体分のmeshのみ受け取る前提
    key, path = list(mesh_paths.items())[0]
    base_name = os.path.basename(path).replace("_mesh.obj", "")
    merged_image_path_jpg = os.path.join(host_input_dir, "front", base_name + ".jpg")
    merged_image_path_png = os.path.join(host_input_dir, "front", base_name + ".png")
    host_mesh_path = convert_to_host_path(path)

    output_file = os.path.join(host_output_dir, "combined_model.glb").replace("\\", "/")

    payload = {
        "type": "execute_code",
        "params": {
            "code": f'''
import bpy
import os

# 既存オブジェクト削除
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# OBJ読み込み
bpy.ops.import_scene.obj(filepath=r"{host_mesh_path}")
objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
if not objs:
    raise RuntimeError("No mesh imported.")
obj = objs[0]
bpy.context.view_layer.objects.active = obj

# Remesh（ボクセル）
bpy.ops.object.modifier_add(type='REMESH')
obj.modifiers["Remesh"].mode = 'VOXEL'
obj.modifiers["Remesh"].voxel_size = 0.01
bpy.ops.object.modifier_apply(modifier="Remesh")

# スムージング
bpy.ops.object.shade_smooth()

# UV展開
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.uv.smart_project(angle_limit=66)
bpy.ops.object.mode_set(mode='OBJECT')

# マテリアルとテクスチャ適用
mat = bpy.data.materials.new(name="AutoMaterial")
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links
bsdf = nodes.get("Principled BSDF")
tex_image = nodes.new('ShaderNodeTexImage')

try:
    if os.path.exists(r"{merged_image_path_jpg}"):
        tex_image.image = bpy.data.images.load(r"{merged_image_path_jpg}")
    elif os.path.exists(r"{merged_image_path_png}"):
        tex_image.image = bpy.data.images.load(r"{merged_image_path_png}")
    else:
        raise FileNotFoundError("Texture not found")
    if bsdf:
        links.new(bsdf.inputs['Base Color'], tex_image.outputs['Color'])
except Exception as e:
    print(f"[WARN] Failed to load texture image:", e)

if obj.data.materials:
    obj.data.materials[0] = mat
else:
    obj.data.materials.append(mat)

# GLBエクスポート
bpy.ops.export_scene.gltf(
    filepath=r"{output_file}",
    export_format='GLB',
    export_materials='EXPORT'
)
'''
        }
    }

    try:
        with socket.create_connection(("host.docker.internal", 9876), timeout=10) as sock:
            sock.sendall(json.dumps(payload).encode('utf-8'))

            response = b''
            sock.settimeout(5)
            while True:
                try:
                    data = sock.recv(4096)
                    if not data:
                        break
                    response += data
                    if b'}' in data:
                        break
                except socket.timeout:
                    break

            result = json.loads(response.decode('utf-8'))

            if result.get("status") != "success":
                raise RuntimeError(f"[ERROR] BlenderMCP error: {result.get('message')}")
            print("[INFO] BlenderMCP execution succeeded")

    except Exception as e:
        print("[ERROR] BlenderMCP call failed during socket communication.")
        raise RuntimeError("Failed to connect to BlenderMCP via socket") from e
