from pydantic import BaseModel
from typing import List, Optional

class Question(BaseModel):
    number: int
    question: str
    solution: str

class Task(BaseModel):
    title: str
    description: str
    questions: List[Question]

class Writeup(BaseModel):
    title: str
    url: str

class Video(BaseModel):
    title: str
    url: str

class Room(BaseModel):
    name: str
    description: str
    room_url: str
    tags: List[str]
    tasks: List[Task]
    writeups: List[Writeup]
    videos: List[Video]

class RoomInDB(Room):
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Basic Pentesting",
                "description": "A beginner-friendly room to learn basic pentesting skills.",
                "room_url": "https://tryhackme.com/room/basicpentesting",
                "tags": ["beginner", "pentesting"],
                "tasks": [
                    {
                        "title": "Task 1",
                        "description": "Find the hidden flag.",
                        "questions": [
                            {"number": 1, "question": "Where is the flag located?", "solution": "In the hidden directory."},
                            {"number": 2, "question": "What is the flag?", "solution": "THM{hidden_flag}"}
                        ]
                    },
                    {
                        "title": "Task 2",
                        "description": "Crack the password hash.",
                        "questions": [
                            {"number": 1, "question": "What is the password hash?", "solution": "5f4dcc3b5aa765d61d8327deb882cf99"},
                            {"number": 2, "question": "What is the cracked password?", "solution": "password"}
                        ]
                    }
                ],
                "writeups": [
                    {"title": "Basic Pentesting Writeup", "url": "https://example.com/writeup1"}
                ],
                "videos": [
                    {"title": "Basic Pentesting Video", "url": "https://example.com/video1"}
                ]
            }
        }

class Submission(BaseModel):
    name: str
    description: str
    room_url: str
    tags: List[str]
    tasks: List[Task]
    writeups: List[Writeup]
    videos: List[Video]
    submitted_by_username: str
    submitted_by_user_socials: Optional[List[str]] = []
    approved: bool = False

class SubmissionInDB(Submission):
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Basic Pentesting",
                "description": "A beginner-friendly room to learn basic pentesting skills.",
                "room_url": "https://tryhackme.com/room/basicpentesting",
                "tags": ["beginner", "pentesting"],
                "tasks": [
                    {
                        "title": "Task 1",
                        "description": "Find the hidden flag.",
                        "questions": [
                            {"number": 1, "question": "Where is the flag located?", "solution": "In the hidden directory."},
                            {"number": 2, "question": "What is the flag?", "solution": "THM{hidden_flag}"}
                        ]
                    },
                    {
                        "title": "Task 2",
                        "description": "Crack the password hash.",
                        "questions": [
                            {"number": 1, "question": "What is the password hash?", "solution": "5f4dcc3b5aa765d61d8327deb882cf99"},
                            {"number": 2, "question": "What is the cracked password?", "solution": "password"}
                        ]
                    }
                ],
                "writeups": [
                    {"title": "Basic Pentesting Writeup", "url": "https://example.com/writeup1"}
                ],
                "videos": [
                    {"title": "Basic Pentesting Video", "url": "https://example.com/video1"}
                ],
                "submitted_by_username": "testuser",
                "submitted_by_user_socials": ["https://twitter.com/testuser"],
                "approved": False
            }
        }