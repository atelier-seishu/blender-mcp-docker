#!/bin/bash
echo "[INFO] Launching BlenderMCP..."
blender --background scripts/base.blend --python scripts/blender_rpc_server.py &

echo "[INFO] Running pipeline..."
python scripts/run_pipeline.py