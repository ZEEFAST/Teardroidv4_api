from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT
from db.database import auth_db
from datetime import datetime

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

class LoginRequest(BaseModel):
    username: str
    password: str

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

class Settings(BaseModel):
    authjwt_secret_key: str = "zeefer-droid-super-secret-key"
    authjwt_access_token_expires: int = 3600

def check_auth():
    data = auth_db.fetch().items
    if len(data) == 0:
        auth_db.put({"username": "flash", "password": "admin"})
    else:
        pass

def check_auth():
    """Initialize default admin account if not exists"""
    try:
        db = auth_db()
        response = db.select("*").eq("username", "admin").execute()
        
        if not response.data or len(response.data) == 0:
            db.insert({
                "username": "admin",
                "password": "admin",
                "created_at": datetime.now().isoformat()
            }).execute()
            print("✓ Default admin account created")
        else:
            print("✓ Admin account already exists")
    except Exception as e:
        print(f"⚠ Auth check failed: {str(e)}")

@router.post("/login")
async def login(credentials: LoginRequest, Authorize: AuthJWT = Depends()):
    """
    Login endpoint - returns JWT token
    
    Default credentials:
    - username: admin
    - password: admin
    """
    try:
        db = auth_db()
        response = db.select("*").eq("username", credentials.username).eq("password", credentials.password).execute()
        
        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        access_token = Authorize.create_access_token(
            subject=credentials.username,
            expires_time=3600
        )
        
        return JSONResponse({
            "success": True,
            "token": access_token,
            "message": "Login successful",
            "user": credentials.username
        })
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login error: {str(e)}")

@router.post("/change-password")
async def change_password(request: ChangePasswordRequest, Authorize: AuthJWT = Depends()):
    """Change user password"""
    try:
        Authorize.jwt_required()
        username = Authorize.get_jwt_subject()
        
        db = auth_db()
        
        # Verify old password
        response = db.select("*").eq("username", username).eq("password", request.old_password).execute()
        
        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=401, detail="Incorrect old password")
        
        # Update password
        user_id = response.data[0]["id"]
        db.update({"password": request.new_password}).eq("id", user_id).execute()
        
        return JSONResponse({
            "success": True,
            "message": "Password changed successfully"
        })
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Initialize auth on startup
check_auth()
