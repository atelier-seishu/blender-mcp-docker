FROM python:3.10-slim

# 基本ツール
RUN apt update && apt install -y git wget unzip curl libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリ
WORKDIR /workspace

# Pythonライブラリ
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# BlenderMCPとTripoSRのclone
RUN git clone https://github.com/ahujasid/blender-mcp.git blender_mcp
RUN git clone https://github.com/VAST-AI-Research/TripoSR.git tripo_sr

# Blender CLIの呼び出しはホストBlenderを使う前提
