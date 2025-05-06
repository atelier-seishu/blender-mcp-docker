FROM python:3.10-slim

# システム依存パッケージのインストール
RUN apt-get update && apt-get install -y \
    git \
    cmake \
    build-essential \
    ninja-build \
    libomp-dev \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*


# CUDAなしのtorch（CPU版）を明示的に指定してインストール
RUN pip install torch==2.1.0+cpu torchvision==0.16.0+cpu torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cpu

# numpy先にインストール（torch内部のwarning回避）
RUN pip install numpy

# torchmcubes のインストール（CPU専用として明示）
RUN pip install git+https://github.com/tatsy/torchmcubes.git --config-settings=cmake.args="-DTORCHMCUBES_CUDA=OFF"

# 作業ディレクトリ
WORKDIR /workspace

# Pythonライブラリのインストール
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN pip install git+https://github.com/tatsy/torchmcubes.git

# BlenderMCP を clone（Docker内に含める）
RUN git clone https://github.com/ahujasid/blender-mcp.git blender_mcp

# TripoSR を clone（Docker内に含める）
RUN git clone https://github.com/VAST-AI-Research/TripoSR.git tripo_sr

# スクリプト追加
COPY scripts /workspace/scripts

# スクリプト実行設定
CMD ["python", "scripts/run_pipeline.py"]
