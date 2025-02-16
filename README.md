# 🌍 位置情報取得システム (FastAPI + Next.js)

📌 **このプロジェクトは、ユーザーの位置情報 (IP / GPS / デバイス情報) を取得し、表示するアプリです。**  
🚀 **バックエンドは FastAPI (Python)、フロントエンドは Next.js (TypeScript) で構築！**

---

## **📌 機能**
✅ **IP アドレス & 位置情報の取得**（`ip-api.com` を使用）  
✅ **GPS 情報の取得**（ブラウザの `navigator.geolocation` を使用）  
✅ **デバイス情報の取得**（OS・ブラウザ・画面サイズ）  
✅ **データベース (PostgreSQL) に位置情報を保存**  
✅ **AWS Lambda + AWS Amplify でデプロイ可能**  

---

## **📌 技術スタック**
### **🟢 フロントエンド (Next.js)**
- **Next.js** (React / TypeScript)
- **Tailwind CSS** (スタイリング)
- **Geolocation API** (GPS 位置情報取得)

### **🔵 バックエンド (FastAPI)**
- **FastAPI** (Python で高速な API)
- **PostgreSQL (AWS RDS)** (位置情報データの保存)
- **SQLAlchemy** (ORM)
- **Serverless Framework** (AWS Lambda デプロイ)
- **`ip-api.com` API** (IP アドレスの位置情報取得)

---

## **📌 ディレクトリ構成**
```sh
/ipget
├── backend               # FastAPI バックエンド
│   ├── database.py       # DB接続 (SQLAlchemy)
│   ├── models.py         # DBモデル
│   ├── routes/           # APIルート
│   ├── server.py         # FastAPI サーバー
│   ├── requirements.txt  # Pythonパッケージ
│   ├── serverless.yml    # AWS Lambda デプロイ設定
│   ├── .env              # 環境変数（ローカル用）
│   └── venv/             # Python仮想環境
└── frontend              # Next.js フロントエンド
    ├── app/              # ページコンポーネント
    ├── public/           # 静的ファイル
    ├── package.json      # Node.js パッケージ
    ├── tailwind.config.js # Tailwind 設定
    └── .env.local        # 環境変数（ローカル用）
```

---

## **📌 環境変数**
### **🔹 `backend/.env`**
```ini
DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DATABASE
AWS_REGION=ap-northeast-1
```

### **🔹 `frontend/.env.local`**
```ini
NEXT_PUBLIC_API_BASE_URL=https://your-api-url.amazonaws.com
```

---

## **📌 セットアップ手順**
### **1️⃣ バックエンド (FastAPI) のセットアップ**
```sh
cd backend
python -m venv venv
source venv/bin/activate  # Windows の場合: `venv\Scripts\activate`
pip install -r requirements.txt
uvicorn server:app --reload
```
➡ **`http://localhost:8000` で FastAPI サーバーが起動！**

---

### **2️⃣ フロントエンド (Next.js) のセットアップ**
```sh
cd frontend
npm install
npm run dev
```
➡ **`http://localhost:3000` で Next.js アプリが起動！**

---

## **📌 API エンドポイント**
| HTTP メソッド | エンドポイント  | 説明 |
|--------------|---------------|-----------------------------|
| **GET** | `/api/location` | ユーザーの位置情報 (IP / GPS) を取得 |
| **POST** | `/api/location` | 位置情報を DB に保存 |

---

## **📌 デプロイ**
### **AWS Lambda (Serverless Framework)**
```sh
cd backend
serverless deploy
```
➡ AWS Lambda にデプロイ完了！

### **AWS Amplify (フロントエンド)**
1. AWS Amplify に GitHub リポジトリを連携
2. **環境変数を設定 (`NEXT_PUBLIC_API_BASE_URL`)**
3. **デプロイを開始**
4. デプロイ完了後、URL を確認

---

## **📌 動作確認**
1️⃣ **フロント (`http://localhost:3000`) にアクセス**  
2️⃣ **「位置情報を取得」ボタンをクリック**  
3️⃣ **ブラウザの開発ツール (`F12 → Network`) で `/api/location` のリクエストを確認**  
4️⃣ **FastAPI (`http://localhost:8000/docs`) の Swagger UI で API をテスト**

---

## **📌 トラブルシューティング**
### **❌ `DATABASE_URL が設定されていません！`**
**解決策:**
- `.env` に `DATABASE_URL` を設定
- AWS Lambda の環境変数に `DATABASE_URL` を追加

### **❌ `ModuleNotFoundError: No module named 'fastapi'`**
**解決策:**
```sh
cd backend
source venv/bin/activate  # 仮想環境を有効化
pip install -r requirements.txt
```

### **❌ `Cannot GET /api/location`**
**解決策:**
- `frontend/.env.local` の `NEXT_PUBLIC_API_BASE_URL` を正しい URL に修正
- `npm run dev` で Next.js を再起動

---

## **📌 まとめ**
| 項目 | 使用技術 |
|------|------------------------------|
| **フロントエンド** | Next.js (React, TypeScript) |
| **バックエンド** | FastAPI (Python) |
| **データベース** | PostgreSQL (AWS RDS) |
| **デプロイ** | AWS Lambda (Serverless) / AWS Amplify |
| **位置情報取得** | `ip-api.com` / `Geolocation API` |

---

🚀 **AWS Lambda + Amplify で動く FastAPI + Next.js の位置情報取得アプリが完成！**  
📌 **エラーが出たら `logs` を確認して試してみてください！**

```sh
# AWS Lambda のログ確認
serverless logs -f app

# Next.js のログ確認
npm run dev
```
