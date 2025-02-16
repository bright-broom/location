from fastapi import APIRouter, Request, Depends
import requests
from sqlalchemy.orm import Session
from database import get_db
from models import Location
import os

router = APIRouter()
IPINFO_API_KEY = os.getenv("IPINFO_API_KEY")

@router.get("/api/location")
async def get_location(request: Request, db: Session = Depends(get_db)):
    """ クライアントのIPを取得し、詳細な位置情報を取得 """

    # ✅ まず `x-forwarded-for` を確認（リバースプロキシ対応）
    ip = request.headers.get("x-forwarded-for", request.client.host)

    # ✅ ローカルIPなら `ipify.org` で外部IPを取得
    if ip.startswith(("127.", "192.168.", "10.")):
        ip = requests.get("https://api64.ipify.org").text

    # ✅ `ip-api.com` で詳細情報を取得
    ip_api_url = f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,zip,lat,lon,isp,org,as,timezone,query"
    ip_api_data = requests.get(ip_api_url).json()

    if ip_api_data["status"] != "success":
        return {"error": "Could not retrieve location", "ip": ip}

    # ✅ `ipinfo.io`（APIキーがある場合のみ）
    ipinfo_data = {}
    if IPINFO_API_KEY:
        ipinfo_url = f"https://ipinfo.io/{ip}/json?token={IPINFO_API_KEY}"
        ipinfo_data = requests.get(ipinfo_url).json()

    # ✅ 取得データを統合
    location_data = {
        "ip": ip,
        "city": ip_api_data.get("city"),
        "region": ip_api_data.get("regionName"),
        "country": ip_api_data.get("country"),
        "postal": ip_api_data.get("zip"),
        "latitude": ip_api_data.get("lat"),
        "longitude": ip_api_data.get("lon"),
        "timezone": ip_api_data.get("timezone"),
        "isp": ip_api_data.get("isp"),
        "org": ip_api_data.get("org"),
        "asn": ip_api_data.get("as"),
        "hostname": ipinfo_data.get("hostname", "N/A") if ipinfo_data else "N/A"
    }

    return location_data


@router.post("/api/location")
async def save_location(data: dict, db: Session = Depends(get_db)):
    """ 位置情報 + デバイス情報をDBに保存 """

    location = Location(
        ip=data["ip"],
        city=data["city"],
        region=data["region"],
        country=data["country"],
        latitude=data["latitude"],
        longitude=data["longitude"],
        postal=data.get("postal"),
        timezone=data.get("timezone"),
        isp=data.get("isp"),
        org=data.get("org"),
        hostname=data.get("hostname"),
        device=data.get("device"),
        os=data.get("os"),
        browser=data.get("browser"),
        screen_size=data.get("screenSize")
    )
    db.add(location)
    db.commit()
    return {"status": "saved"}
