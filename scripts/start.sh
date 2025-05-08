
#!/bin/bash
# scripts/start.sh

echo "[INFO] Launching BlenderMCP (9876)..."
blender --background --python scripts/blender_rpc_server.py &

echo "[INFO] Running pipeline..."
python scripts/run_pipeline.py
