from fastapi import APIRouter, Request, Depends, HTTPException
import httpx
import asyncio
from sqlalchemy.orm import Session
from database import get_db
from models import Location
import os

router = APIRouter()
IPINFO_API_KEY = os.getenv("IPINFO_API_KEY")

async def fetch_json(url: str) -> dict:
    """指定されたURLから非同期でJSONデータを取得"""
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
    except (httpx.RequestError, ValueError):
        return {}

async def fetch_text(url: str) -> str:
    """指定されたURLから非同期でプレーンテキストデータを取得"""
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.text.strip()
    except httpx.RequestError:
        return "unknown"

@router.get("/api/location")
async def get_location(request: Request, db: Session = Depends(get_db)):
    """ クライアントのIPを取得し、詳細な位置情報を取得 """

    # `x-forwarded-for` でIPを取得（リバースプロキシ対応）
    ip = request.headers.get("x-forwarded-for") or request.client.host

    # ローカルIPなら外部IPを取得（修正済み）
    if ip.startswith(("127.", "192.168.", "10.")):
        ip = await fetch_text("https://api64.ipify.org")

    # 並列で `ip-api.com` と `ipinfo.io` のリクエストを送る
    ip_api_url = f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,zip,lat,lon,isp,org,as,timezone,query"
    ipinfo_url = f"https://ipinfo.io/{ip}/json?token={IPINFO_API_KEY}" if IPINFO_API_KEY else None

    tasks = [fetch_json(ip_api_url)]
    if ipinfo_url:
        tasks.append(fetch_json(ipinfo_url))

    results = await asyncio.gather(*tasks)

    # APIレスポンスの取得
    ip_api_data = results[0]
    ipinfo_data = results[1] if len(results) > 1 else {}

    if ip_api_data.get("status") != "success":
        raise HTTPException(status_code=500, detail="位置情報の取得に失敗しました")

    # 取得データを統合
    return {
        "ip": ip,
        "city": ip_api_data.get("city", "unknown"),
        "region": ip_api_data.get("regionName", "unknown"),
        "country": ip_api_data.get("country", "unknown"),
        "postal": ip_api_data.get("zip", ""),
        "latitude": ip_api_data.get("lat", 0.0),
        "longitude": ip_api_data.get("lon", 0.0),
        "timezone": ip_api_data.get("timezone", ""),
        "isp": ip_api_data.get("isp", ""),
        "org": ip_api_data.get("org", ""),
        "asn": ip_api_data.get("as", ""),
        "hostname": ipinfo_data.get("hostname", "N/A"),
    }
