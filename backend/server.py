from fastapi import FastAPI, Response
from mangum import Mangum  # AWS Lambda 互換
from database import engine, Base
from routes import location
from fastapi.middleware.cors import CORSMiddleware

# DB テーブル作成（本番では Alembic のマイグレーション推奨）
Base.metadata.create_all(bind=engine)

# FastAPI アプリの初期化
app = FastAPI()

# CORS 設定（Next.js との通信を許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要ならドメインを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルート登録
app.include_router(location.router)

# `favicon.ico` のリクエストを無視
@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)  # No Content

# ヘルスチェック API
@app.get("/")
async def root():
    return {"message": "FastAPI on AWS Lambda"}

# AWS Lambda 用のエントリーポイント
lambda_handler = Mangum(app)
