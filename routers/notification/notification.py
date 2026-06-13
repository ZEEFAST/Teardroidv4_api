from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT
from db.database import notification_db
from datetime import datetime
import uuid

router = APIRouter(
    prefix="/notification",
    tags=["notification"],
)

class NotificationData(BaseModel):
    device_id: str
    package_name: str
    title: str
    body: str

@router.post("/add")
async def add_notification(notification: NotificationData):
    """Add notification from device"""
    try:
        db = notification_db()
        
        # Check if notification already exists (avoid duplicates)
        existing = db.select("*").eq("device_id", notification.device_id).eq("package_name", notification.package_name).eq("title", notification.title).execute()
        
        if existing.data and len(existing.data) > 0:
            return JSONResponse({
                "success": False,
                "message": "Notification already exists"
            })
        
        data = {
            "id": str(uuid.uuid4()),
            "device_id": notification.device_id,
            "package_name": notification.package_name,
            "title": notification.title,
            "body": notification.body,
            "read": False,
            "created_at": datetime.now().isoformat()
        }
        
        response = db.insert(data).execute()
        
        return JSONResponse({
            "success": True,
            "notification_id": response.data[0]["id"],
            "message": "Notification added successfully"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/device/{device_id}")
async def get_notifications(device_id: str, Authorize: AuthJWT = Depends()):
    """Get notifications for device"""
    try:
        Authorize.jwt_required()
        
        db = notification_db()
        response = db.select("*").eq("device_id", device_id).order("created_at", desc=True).execute()
        
        return JSONResponse({
            "success": True,
            "total": len(response.data),
            "notifications": response.data
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/")
async def get_all_notifications(Authorize: AuthJWT = Depends()):
    """Get all notifications"""
    try:
        Authorize.jwt_required()
        
        db = notification_db()
        response = db.select("*").order("created_at", desc=True).execute()
        
        return JSONResponse({
            "success": True,
            "total": len(response.data),
            "notifications": response.data
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.put("/mark-read/{notification_id}")
async def mark_notification_read(notification_id: str, Authorize: AuthJWT = Depends()):
    """Mark notification as read"""
    try:
        Authorize.jwt_required()
        
        db = notification_db()
        db.update({"read": True}).eq("id", notification_id).execute()
        
        return JSONResponse({
            "success": True,
            "message": "Notification marked as read"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.delete("/device/{device_id}")
async def delete_device_notifications(device_id: str, Authorize: AuthJWT = Depends()):
    """Delete all notifications for device"""
    try:
        Authorize.jwt_required()
        
        db = notification_db()
        db.delete().eq("device_id", device_id).execute()
        
        return JSONResponse({
            "success": True,
            "message": "Notifications deleted successfully"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
