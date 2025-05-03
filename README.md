# blender-mcp-docker

## セットアップ手順（Windows Terminal で実行）

```bash
cd blender-mcp-docker
docker compose up --build -d
```

起動後、http://localhost:3000 で MCP サーバーが動作

Blender の MCP アドオンから「Connect to Claude」などを押すと連携可能

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