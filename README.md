# 🌍 位置情報取得システム (FastAPI + Next.js)

📌 **このプロジェクトは、ユーザーの位置情報 (IP / GPS / デバイス情報) を取得し、表示するアプリです。**  
🚀 **バックエンドは FastAPI (Python)、フロントエンドは Next.js (TypeScript) で構築！**

---

## **📌 機能**
✅ **IP アドレス & 位置情報の取得**（`ip-api.com` を使用）  
✅ **IPv6 対応**（`api64.ipify.org` を使用）  
✅ **GPS 情報の取得**（ブラウザの `navigator.geolocation` を使用）  
✅ **デバイス情報の取得**（OS・ブラウザ・画面サイズ）  
✅ **データベース (PostgreSQL) に位置情報を保存**  
✅ **バックエンド (FastAPI) & フロントエンド (Next.js) の連携**  
✅ **非同期処理 (`httpx` + `asyncio.gather()`) により高速化**  
✅ **Vercel / Railway でデプロイ可能**

---

## **📌 技術スタック**
### **🟢 フロントエンド (Next.js)**
- **Next.js** (React / TypeScript)
- **Tailwind CSS** (スタイリング)
- **Geolocation API** (GPS 位置情報取得)

### **🔵 バックエンド (FastAPI)**
- **FastAPI** (Python で高速な API)
- **PostgreSQL** (位置情報データの保存)
- **SQLAlchemy** (ORM)
- **`ip-api.com` API** (IP アドレスの位置情報取得)
- **非同期 API (`httpx`) による高速処理**
- **エラーハンドリングの強化 (`try-except`)**
- **`asyncio.gather()` による並列リクエスト処理**
