import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://toshikisakuta@localhost/location_db")

# PostgreSQL のエンジン作成
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# DB セッション取得
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
