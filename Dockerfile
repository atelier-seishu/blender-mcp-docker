FROM python:3.10-slim

# 基本ツール
RUN apt update && apt install -y git wget unzip curl libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリ
WORKDIR /workspace

# Pythonライブラリのインストール
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# コード類のコピー
COPY . .

# BlenderMCPとTripoSRのclone（TripoSRはsetupがないのでinstall不要）
RUN git clone https://github.com/ahujasid/blender-mcp.git blender_mcp
RUN git clone https://github.com/VAST-AI-Research/TripoSR.git tripo_sr

# 実行スクリプト
CMD ["python", "scripts/run_pipeline.py"]