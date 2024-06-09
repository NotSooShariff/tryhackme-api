from fastapi import FastAPI, Depends, HTTPException, status, Request, Query
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pymongo import MongoClient
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import time
import uvicorn
from fastapi.responses import JSONResponse
from typing import Optional
import logging
from src.models import Submission, SubmissionInDB

load_dotenv()

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": "Rate limit exceeded. Try again later."},
    )

# This will throw an error if you haven't properly setup a .env file
client = MongoClient(os.getenv("MONGODB_URL"))
db = client.tryhackme

security = HTTPBasic()

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def log_request(request: Request):
    ip = request.client.host
    request_data = {
        "path": request.url.path,
        "method": request.method,
        "client_ip": ip,
        "timestamp": time.time()
    }
    db.request_logs.insert_one(request_data)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    log_request(request)
    response = await call_next(request)
    return response


def get_current_username(credentials: HTTPBasicCredentials = Depends(security), request: Request = None):
    correct_username = os.getenv("ADMIN_USERNAME")
    correct_password = os.getenv("ADMIN_PASSWORD")
    if credentials.username != correct_username or credentials.password != correct_password:
        log_failed_attempt(request, credentials.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

def log_failed_attempt(request: Request, username: str):
    ip = request.client.host  
    db.authlog.insert_one({"username": username, "ip": ip, "timestamp": time.time()})

    failed_attempts = db.authlog.count_documents({
        "ip": ip,
        "timestamp": {"$gt": time.time() - 600}
    })
    if failed_attempts > 5:
        db.banned_ips.insert_one({"ip": ip, "timestamp": time.time()})

class Room(BaseModel):
    name: str
    description: str
    room_url: str
    tags: Optional[list[str]]
    tasks: Optional[list[dict]]
    writeups: Optional[list[dict]]
    videos: Optional[list[dict]]


@app.get("/rooms", response_model=list[Room])
@limiter.limit("5/minute")
async def get_rooms(request: Request):
    rooms = list(db.rooms.find())
    return rooms

@app.get("/room/{name}", response_model=Room)
@limiter.limit("5/minute")
async def get_room(name: str, request: Request):
    room = db.rooms.find_one({"name": name})
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@app.post("/room", dependencies=[Depends(get_current_username)])
@limiter.limit("5/minute")
async def create_room(room: Room, request: Request):
    db.rooms.insert_one(room.dict())
    return {"message": "Room created successfully"}

@app.put("/room/{name}", dependencies=[Depends(get_current_username)])
@limiter.limit("5/minute")
async def update_room(name: str, room: Room, request: Request):
    db.rooms.update_one({"name": name}, {"$set": room.dict()})
    return {"message": "Room updated successfully"}

@app.delete("/room/{name}", dependencies=[Depends(get_current_username)])
@limiter.limit("5/minute")
async def delete_room(name: str, request: Request):
    db.rooms.delete_one({"name": name})
    return {"message": "Room deleted successfully"}

@app.get("/search", response_model=list[Room])
@limiter.limit("5/minute")
async def search_rooms(request: Request, keyword: str = Query(..., min_length=1)):
    keyword_regex = {"$regex": keyword, "$options": "i"}
    rooms = list(db.rooms.find({"$or": [{"name": keyword_regex}, {"description": keyword_regex}]}))
    return rooms

@app.get("/room_by_url", response_model=Room)
@limiter.limit("5/minute")
async def get_room_by_url(request: Request, room_url: str = Query(...)):
    room = db.rooms.find_one({"room_url": room_url})
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@app.post("/submit", response_model=Submission)
async def submit_solution(submission: SubmissionInDB):
    submission_data = submission.dict()
    db.submissions.insert_one(submission_data)
    return

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

