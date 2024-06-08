import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URL"))
db = client.tryhackme

rooms = [
    {
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
    },
    {
        "name": "Intermediate Hacking",
        "description": "An intermediate-level room to improve your hacking skills.",
        "room_url": "https://tryhackme.com/room/intermediatehacking",
        "tags": ["intermediate", "hacking"],
        "tasks": [
            {
                "title": "Task 1",
                "description": "Exploit the web application.",
                "questions": [
                    {"number": 1, "question": "What is the vulnerability?", "solution": "SQL Injection"},
                    {"number": 2, "question": "How to exploit it?", "solution": "Use ' OR 1=1 --"}
                ]
            },
            {
                "title": "Task 2",
                "description": "Escalate privileges.",
                "questions": [
                    {"number": 1, "question": "What is the exploit?", "solution": "Buffer Overflow"},
                    {"number": 2, "question": "What is the privilege level?", "solution": "Root"}
                ]
            }
        ],
        "writeups": [
            {"title": "Intermediate Hacking Writeup", "url": "https://example.com/writeup2"}
        ],
        "videos": [
            {"title": "Intermediate Hacking Video", "url": "https://example.com/video2"}
        ]
    },
    {
        "name": "Advanced Exploitation",
        "description": "A challenging room for advanced users to practice exploitation techniques.",
        "room_url": "https://tryhackme.com/room/advancedexploitation",
        "tags": ["advanced", "exploitation"],
        "tasks": [
            {
                "title": "Task 1",
                "description": "Bypass the firewall.",
                "questions": [
                    {"number": 1, "question": "How to bypass the firewall?", "solution": "Use a VPN."},
                    {"number": 2, "question": "What is the IP address?", "solution": "192.168.1.1"}
                ]
            },
            {
                "title": "Task 2",
                "description": "Exploit the buffer overflow vulnerability.",
                "questions": [
                    {"number": 1, "question": "What is the vulnerable function?", "solution": "strcpy"},
                    {"number": 2, "question": "What is the payload?", "solution": "shellcode"}
                ]
            }
        ],
        "writeups": [
            {"title": "Advanced Exploitation Writeup", "url": "https://example.com/writeup3"}
        ],
        "videos": [
            {"title": "Advanced Exploitation Video", "url": "https://example.com/video3"}
        ]
    }
]

db.rooms.insert_many(rooms)
print("Database populated with example rooms.")
