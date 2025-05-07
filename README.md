# (WIP)blender-mcp-docker

## 概要

```txt
┌────────────────────┐
│ ユーザーが三面図を投入│
└────────┬────────────┘
         ▼
┌───────────────────────────────────────────────┐
│ Dockerコンテナ (model_pipeline)                                      │
│ - run_pipeline.py（エントリーポイント）                        │
│ - tripo_wrapper.py（TripoSR 呼び出し）                     │
│ - blender_rpc.py（FastAPI 経由で Blender に RPC） │
│ - TripoSR モデル一式 + BlenderMCP server構築済 │
└────────┬──────────────────────────────────────┘
         ▼
┌──────────────────────────┐
│ Docker外：ローカルBlender │
│ - Blender + BlenderMCPアドオン │
└──────────────────────────┘
         ▼
     モデル完成 → data/output に.obj/.fbx等出力
```

## 使用フロー
ユーザーが data/input に3面図画像（front, side, back）を配置

docker-compose up で model_pipeline を起動

run_pipeline.py が起動し、画像を TripoSR に渡してメッシュ生成

生成メッシュを ソケット通信 経由でローカルの Blender に渡す（POST /process）

Blender内のBlenderMCPアドオンが処理してモデル出力（data/outputへ）

完了通知 or ログ出力で処理確認



## 利用方法イメージ
### ① BlenderをホストOSで起動
起動確認だけでなく、**BlenderのバージョンがMCPに対応（例: 4.4.1）**していることも確認してください。

### ② BlenderにBlenderMCPアドオンがインストール・有効化されているか確認

アドオン名：BlenderMCP

F4 > Preferences > Add-ons > BlenderMCP にてインストール・チェックボックスON

Blender起動後、自動で port 9876 にてRPC待ち受け状態になる（※設定で有効になっていれば）

📌 もし自動起動されない場合、スクリプトなどでRPC起動する必要あり：

```python
import blender_mcp.server
blender_mcp.server.serve(port=9876)
```

### ③ docker-compose up にてコンテナ起動

TripoSRモデル処理が始まり、メッシュファイルが data/tmp/{stem}_mesh.obj に保存される。

その後 run_mcp.py が blender_rpc.Client('host.docker.internal', 9876) に接続する。

```
📌 host.docker.internal は Docker for Windows/macOS で ホストのIPを指す名前解決済みホスト名です。
→ blender_rpc.py 内で socket.create_connection(("host.docker.internal", 9876)) を行うことでホストBlenderに接続可能。
```

### ④ コンテナ内の run_mcp.py からホストの Blender にRPCで接続

Blender上で実行されるMCPアドオンがメッシュを加工

run_pipeline.py → run_blender_mcp() → run_mcp.py → blender_rpc.Client → Blender

## 構成
```
project-root/
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── data/
│   ├── input/         ← 3面図イラスト投入先
│   ├── output/        ← 出力glb/obj保存先
│   └── tmp/           ← 一時処理ファイル
├── scripts/
│   ├── run_pipeline.py  ← 自動処理フローの本体
│   └── tripo_wrapper.py ← TripoSR実行
```

## Docker手順

実行手順（手動確認用）
data/input/ に3面図の正面画像（例：front_view.png）を配置する

Dockerコンテナを起動

```bash
docker compose up --build
```

別ターミナルでDocker内に入る

```bash
docker exec -it model-generator bash
```
パイプラインを実行する

```bash
python scripts/run_pipeline.py
```

TripoSR によって data/output/model.obj が生成されます。

blender_rpc_server.py を以下のように実行（BlenderのScriptingタブ内で）：

```bash
blender --background --python blender_rpc_server.py -- --port 9876
```

## セットアップ手順（Windows Terminal で実行）

```bash
cd blender-mcp-docker
docker compose up --build -d
```

起動後、http://localhost:3000 で MCP サーバーが動作

Blender の MCP アドオンから「Connect to Claude」などを押すと連携可能

```bash
-- サーバー停止
docker compose down
-- サーバー一時停止
docker compose stop
-- サーバー始動
docker compose start
-- サーバー状況確認
docker compose ps
-- 不要になった場合の完全クリーン
docker compose down --volumes --remove-orphans
-- キャッシュ参照無しでビルド
docker compose build --no-cache
```

## Blender 側の設定ヒント

Blender MCP アドオンの設定が必要な場合は、以下のように mcp.json（Windowsユーザーディレクトリなどに設置）に明記：

```json
{
  "mcpServers": {
    "blender": {
      "command": "curl",
      "args": ["http://localhost:3000"]
    }
  }
}
```

## 前提の環境構築（おまけ）
### ① Docker Desktop のインストール（WSL2対応）

以下のリンクから Docker Desktop をダウンロード・インストール

https://www.docker.com/products/docker-desktop/

インストール時に「WSL2バックエンドを有効にする」にチェックを入れておく

Windows Terminal で確認（再起動後）

```bash
wsl --version
docker --version
```

Docker Desktop を起動し、正常に動いていることを確認

### ② Blender のインストール（Windows）

以下のリンクから Blender をダウンロード（3.x系）

https://www.blender.org/download/

インストーラを実行し、Windows にインストール

起動確認（起動後、「Edit → Preferences → Add-ons」タブを確認）

### ③ Blender MCP アドオンの導入

GitHub から Clone：

https://github.com/ahujasid/blender-mcp/

Blender 起動 → Edit → Preferences → Add-ons → Install...

上記 addon.py を選択して読み込み → 「Interface: Blender MCP」を有効化

サイドバー（Nキー）に「BlenderMCP」タブが追加されていることを確認
