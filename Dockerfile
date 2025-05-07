# --------------------------
# ベースイメージ：Python 3.10 slim
# --------------------------
FROM python:3.10-slim

# --------------------------
# システム依存パッケージのインストール
# OpenGL, glib, CMake, Ninja, OpenMPなど必要ライブラリ
# --------------------------
RUN apt-get update && apt-get install -y \
    git \
    cmake \
    build-essential \
    ninja-build \
    libomp-dev \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# --------------------------
# PyTorch（CPU版）をインストール
# TripoSR要件に合わせた固定バージョン
# --------------------------
RUN pip install torch==2.1.0+cpu torchvision==0.16.0+cpu torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cpu

# --------------------------
# NumPyを先に入れる（PyTorch内部の初期化警告対策）
# --------------------------
RUN pip install numpy

# --------------------------
# torchmcubes（CPU専用）のインストール
# CUDAサポート無効化
# --------------------------
RUN pip install git+https://github.com/tatsy/torchmcubes.git --config-settings=cmake.args="-DTORCHMCUBES_CUDA=OFF"

# --------------------------
# 作業ディレクトリの設定
# --------------------------
WORKDIR /workspace

# --------------------------
# Pythonライブラリのインストール（FastAPI, uvicorn, trimeshなども含める）
# --------------------------
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# --------------------------
# BlenderMCP（非改変）をCloneして配置
# ※/workspace/blender_mcp に設置される想定で使用
# --------------------------
RUN git clone https://github.com/ahujasid/blender-mcp.git /workspace/blender_mcp

# --------------------------
# TripoSR をCloneして配置
# --------------------------
RUN git clone https://github.com/VAST-AI-Research/TripoSR.git tripo_sr

# --------------------------
# スクリプト群を配置
# - scripts/run_pipeline.py（起動スクリプト）
# - scripts/blender_rpc_server.py（FastAPIサーバー）
# - scripts/tripo_wrapper.py（TripoSR実行）
# --------------------------
COPY scripts /workspace/scripts

# --------------------------
# CMD（コンテナ起動時）
# run_pipeline.py から FastAPI + TripoSR 処理を一括起動
# --------------------------
CMD ["python", "scripts/run_pipeline.py"]
    