from fastapi import APIRouter, Request, Depends, HTTPException
import requests
from sqlalchemy.orm import Session
from database import get_db
from models import Location
import os

router = APIRouter()
IPINFO_API_KEY = os.getenv("IPINFO_API_KEY")

@router.get("/api/location")
async def get_location(request: Request, db: Session = Depends(get_db)):
    """
    クライアントのIPを取得し、詳細な位置情報を取得
    """
    # クライアントのIP取得
    ip = request.headers.get("x-forwarded-for", request.client.host)

    # ローカルIPの場合、外部IPを取得
    if ip.startswith(("127.", "192.168.", "10.")):
        try:
            ip = requests.get("https://api64.ipify.org").text
        except requests.RequestException:
            raise HTTPException(status_code=500, detail="外部IPの取得に失敗しました")

    # `ip-api.com` から位置情報を取得
    ip_api_url = f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,zip,lat,lon,isp,org,as,timezone,query"
    try:
        ip_api_response = requests.get(ip_api_url)
        ip_api_data = ip_api_response.json()
    except requests.RequestException:
        raise HTTPException(status_code=500, detail="IP情報の取得に失敗しました")

    if ip_api_data.get("status") != "success":
        return {"error": "位置情報を取得できませんでした", "ip": ip}

    # `ipinfo.io` から追加情報を取得
    ipinfo_data = {}
    if IPINFO_API_KEY:
        try:
            ipinfo_url = f"https://ipinfo.io/{ip}/json?token={IPINFO_API_KEY}"
            ipinfo_response = requests.get(ipinfo_url)
            ipinfo_data = ipinfo_response.json()
        except requests.RequestException:
            ipinfo_data = {}

    # 取得データを統合
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
    """
    位置情報 + デバイス情報をDBに保存
    """
    try:
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
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
