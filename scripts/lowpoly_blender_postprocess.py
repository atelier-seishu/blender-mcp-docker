# scripts/lowpoly_blender_postprocess.py
import bpy
import sys

argv = sys.argv
argv = argv[argv.index("--") + 1:] if "--" in argv else []

if len(argv) != 1:
    print("[ERROR] .obj ファイルパスが必要です")
    sys.exit(1)

obj_path = argv[0]

# 全オブジェクトを削除
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# OBJ読み込み
bpy.ops.import_scene.obj(filepath=obj_path)

# ローポリ + スムース適用
for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        bpy.context.view_layer.objects.active = obj

        decimate = obj.modifiers.new(name="Decimate", type='DECIMATE')
        decimate.ratio = 0.2
        bpy.ops.object.modifier_apply(modifier="Decimate")

        smooth = obj.modifiers.new(name="Smooth", type='SMOOTH')
        smooth.iterations = 5
        bpy.ops.object.modifier_apply(modifier="Smooth")

# 元の.objに上書き保存
bpy.ops.export_scene.obj(filepath=obj_path, use_selection=True)
