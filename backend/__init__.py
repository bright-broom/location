# backend/__init__.py

import os
from dotenv import load_dotenv

# `.env` をロード（ローカル開発用）
load_dotenv()

# 必要な環境変数の存在をチェック
REQUIRED_ENV_VARS = ["DATABASE_URL"]
for var in REQUIRED_ENV_VARS:
    if not os.getenv(var):
        raise ValueError(f"❌ 環境変数 {var} が設定されていません！")

# `backend` を Python モジュールとして認識させる
__all__ = ["database", "models", "routes", "server"]
