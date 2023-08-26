FROM mcr.microsoft.com/devcontainers/python:3.11-bullseye


# 必要なツールをインストール
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*