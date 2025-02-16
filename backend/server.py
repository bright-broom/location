from fastapi import FastAPI
from mangum import Mangum  # Lambda 互換のために必要
from database import engine, Base
from routes import location
from fastapi.middleware.cors import CORSMiddleware

# DBテーブル作成
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS設定（Next.js との通信を許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要ならドメインを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルート登録
app.include_router(location.router)

@app.get("/")
async def root():
    return {"message": "FastAPI on AWS Lambda"}

# AWS Lambda 用の `lambda_handler`
lambda_handler = Mangum(app)
