# furocya-tohenkan (フロ変)

C言語のソースコードからフローチャートを生成し、PDFとして閲覧・ダウンロードできる
FastAPI アプリです。Web UI から .c をアップロードすると、Graphviz で図を描画します。

## デモ

- https://furohen.srnns.com

## 主な機能

- .c ファイルのアップロードとPDF化
- Web UI でのプレビュー
- API からの取得（閲覧/ダウンロード）

## 画面

- `GET /` で Web UI（`web/index.html`）を提供します

## 使い方（ローカル）

### 1) 依存関係の準備

- Python 3.10+
- Graphviz（`dot` コマンドが必要）

### 2) セットアップ

`uv` を使う場合:

```bash
uv sync
```

### 3) 起動

```bash
uvicorn api.main:app --host 0.0.0.0 --port 568
```

ブラウザで `http://localhost:568/` を開き、`.c` をアップロードしてください。

## Docker で起動

```bash
docker compose up -d --build
```

`http://localhost:568/` にアクセスできます。

## API

### POST /upload

- `multipart/form-data` で `.c` ファイルを送信
- `Accept: application/json` を指定すると JSON を返します

レスポンス例:

```json
{
  "view": "/view/<uid>",
  "download": "/download/<uid>"
}
```

### GET /view/{uid}

- PDF をインライン表示（ブラウザプレビュー用）

### GET /download/{uid}

- PDF をダウンロード（元のファイル名を優先）

## 開発メモ

- 変換結果は `work/` に保存されます（起動時に自動作成）
- 変換の中心ロジックは `furohen/` 以下にあります
