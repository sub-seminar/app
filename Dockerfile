# ベースイメージとしてPython 3.9を使用
FROM python:3.9-slim


# システムの依存関係をインストール
RUN apt-get update && apt-get install -y \
    sqlite3 \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*


# 作業ディレクトリを設定
WORKDIR /app

# 必要なライブラリをインストールするためにrequirements.txtをコピー
COPY requirements.txt requirements.txt

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースコードをコピー
COPY . .

# 環境変数を設定
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5050  

# Flaskアプリケーションを実行
CMD ["flask", "run"]
