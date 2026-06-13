from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT
from db.database import command_db, client_db
from datetime import datetime
import uuid

router = APIRouter(
    prefix="/command",
    tags=["command"],
)

class CommandRequest(BaseModel):
    device_id: str
    command: str
    shell: str = None
    number: str = None
    data: str = None

class CommandComplete(BaseModel):
    command_id: str
    response: str = None
    success: bool = True

@router.post("/send")
async def send_command(req: CommandRequest, Authorize: AuthJWT = Depends()):
    """Send command to device"""
    try:
        Authorize.jwt_required()
        
        db = command_db()
        cdb = client_db()
        
        # Verify device exists
        device = cdb.select("*").eq("id", req.device_id).execute()
        if not device.data:
            raise HTTPException(status_code=404, detail="Device not found")
        
        data = {
            "id": str(uuid.uuid4()),
            "device_id": req.device_id,
            "command": req.command,
            "shell": req.shell,
            "number": req.number,
            "data": req.data,
            "is_complete": False,
            "success": False,
            "response": None,
            "created_at": datetime.now().isoformat(),
            "completed_at": None
        }
        
        response = db.insert(data).execute()
        
        return JSONResponse({
            "success": True,
            "command_id": response.data[0]["id"],
            "message": "Command sent successfully"
        })
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/device/{device_id}")
async def get_pending_commands(device_id: str):
    """Get pending commands for device"""
    try:
        db = command_db()
        cdb = client_db()
        
        # Update last_online
        cdb.update({"last_online": datetime.now().isoformat()}).eq("id", device_id).execute()
        
        response = db.select("*").eq("device_id", device_id).eq("is_complete", False).execute()
        
        return JSONResponse({
            "success": True,
            "commands": response.data
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.post("/complete")
async def complete_command(req: CommandComplete):
    """Mark command as complete"""
    try:
        db = command_db()
        
        db.update({
            "is_complete": True,
            "response": req.response,
            "success": req.success,
            "completed_at": datetime.now().isoformat()
        }).eq("id", req.command_id).execute()
        
        return JSONResponse({
            "success": True,
            "message": "Command marked as complete"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/response/{command_id}")
async def get_command_response(command_id: str, Authorize: AuthJWT = Depends()):
    """Get command response"""
    try:
        Authorize.jwt_required()
        
        db = command_db()
        response = db.select("*").eq("id", command_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Command not found")
        
        return JSONResponse({
            "success": True,
            "command": response.data[0]
        })
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/history/{device_id}")
async def get_command_history(device_id: str, Authorize: AuthJWT = Depends()):
    """Get command history for device"""
    try:
        Authorize.jwt_required()
        
        db = command_db()
        response = db.select("*").eq("device_id", device_id).order("created_at", desc=True).execute()
        
        return JSONResponse({
            "success": True,
            "total": len(response.data),
            "commands": response.data
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
