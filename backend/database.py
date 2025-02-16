import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ✅ `.env` をロード（ローカル開発用）
load_dotenv()

# ✅ 環境変数 `DATABASE_URL` を取得
DATABASE_URL = os.getenv("DATABASE_URL")

# ✅ Railway の場合、環境変数が正しく設定されているか確認
if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL が設定されていません！Railway の環境変数を確認してください。")

# ✅ PostgreSQL のエンジンを作成（Railway 用に `pool_pre_ping=True` を追加）
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# ✅ セッションの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ SQLAlchemy のベースクラス
Base = declarative_base()

# ✅ FastAPI の依存性注入用に DB セッションを管理
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
