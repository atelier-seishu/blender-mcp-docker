# --------------------------
# ベースイメージ：Python 3.10 slim
# --------------------------
FROM python:3.10-slim

# --------------------------
# システム依存パッケージ + Blender依存ライブラリ
# --------------------------
RUN apt-get update && apt-get install -y \
    git \
    cmake \
    build-essential \
    ninja-build \
    libomp-dev \
    libgl1 \
    libglib2.0-0 \
    libxrender1 \
    libx11-6 \
    libxi6 \
    libxxf86vm1 \
    libxrandr2 \
    libxfixes3 \
    libxcursor1 \
    libxinerama1 \
    libgl1-mesa-glx \
    libdbus-1-3 \
    libfontconfig1 \
    libfreetype6 \
    libsm6 \
    libxkbcommon0 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# --------------------------
# Blenderのインストール（CLI用）
# --------------------------
RUN wget https://ftp.halifax.rwth-aachen.de/blender/release/Blender3.6/blender-3.6.2-linux-x64.tar.xz \
    && tar -xf blender-3.6.2-linux-x64.tar.xz \
    && mv blender-3.6.2-linux-x64 /opt/blender \
    && ln -s /opt/blender/blender /usr/local/bin/blender \
    && rm blender-3.6.2-linux-x64.tar.xz

# --------------------------
# PyTorch（CPU版）
# --------------------------
RUN pip install torch==2.1.0+cpu torchvision==0.16.0+cpu torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cpu

# --------------------------
# NumPy（警告回避用）
# --------------------------
RUN pip install numpy

# --------------------------
# torchmcubes（CPU専用）
# --------------------------
RUN pip install git+https://github.com/tatsy/torchmcubes.git --config-settings=cmake.args="-DTORCHMCUBES_CUDA=OFF"

# --------------------------
# 作業ディレクトリとPythonパッケージ
# --------------------------
WORKDIR /workspace
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# --------------------------
# BlenderMCP + TripoSR + スクリプト群配置
# --------------------------
RUN git clone https://github.com/ahujasid/blender-mcp.git /workspace/blender_mcp
RUN git clone https://github.com/VAST-AI-Research/TripoSR.git tripo_sr
COPY scripts /workspace/scripts

# --------------------------
# 起動スクリプト追加（BlenderMCP + run_pipeline 並列実行）
# --------------------------
RUN echo '#!/bin/bash\n' \
            'blender --background --python scripts/blender_rpc_server.py &\n' \
            'python scripts/run_pipeline.py\n' > /workspace/scripts/start.sh \
    && chmod +x /workspace/scripts/start.sh

# --------------------------
# エントリポイント
# --------------------------
CMD ["/workspace/scripts/start.sh"]
    