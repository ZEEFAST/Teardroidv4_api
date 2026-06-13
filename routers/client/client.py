from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT
from db.database import client_db
from datetime import datetime

router = APIRouter(
    prefix="/client",
    tags=["client"],
)

class ClientInfo(BaseModel):
    android_version: str
    device_name: str
    sim_operator: str
    sim_country: str
    interval: int = 3000
    active: bool = True

@router.post("/add")
async def add_client(client_info: ClientInfo):
    """Register a new client device"""
    try:
        db = client_db()
        
        data = {
            "android_version": client_info.android_version,
            "device_name": client_info.device_name,
            "sim_operator": client_info.sim_operator,
            "sim_country": client_info.sim_country,
            "interval": client_info.interval,
            "active": client_info.active,
            "last_online": datetime.now().isoformat(),
            "created_at": datetime.now().isoformat()
        }
        
        response = db.insert(data).execute()
        
        return JSONResponse({
            "success": True,
            "device_id": response.data[0]["id"] if response.data else None,
            "message": "Client registered successfully"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/")
async def get_all_clients(Authorize: AuthJWT = Depends()):
    """Get all registered clients"""
    try:
        Authorize.jwt_required()
        
        db = client_db()
        response = db.select("*").order("last_online", desc=True).execute()
        
        return JSONResponse({
            "success": True,
            "total": len(response.data),
            "clients": response.data
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/device/{device_id}")
async def get_client(device_id: str, Authorize: AuthJWT = Depends()):
    """Get specific client device info"""
    try:
        Authorize.jwt_required()
        
        db = client_db()
        response = db.select("*").eq("id", device_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Device not found")
        
        # Update last_online
        db.update({"last_online": datetime.now().isoformat()}).eq("id", device_id).execute()
        
        return JSONResponse({
            "success": True,
            "client": response.data[0]
        })
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.delete("/device/{device_id}")
async def delete_client(device_id: str, Authorize: AuthJWT = Depends()):
    """Delete a client device"""
    try:
        Authorize.jwt_required()
        
        db = client_db()
        db.delete().eq("id", device_id).execute()
        
        return JSONResponse({
            "success": True,
            "message": "Device deleted successfully"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
