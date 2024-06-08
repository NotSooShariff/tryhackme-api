from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URL"))
db = client.tryhackme

def delete_all_rooms():
    result = db.rooms.delete_many({})
    print(f"Deleted {result.deleted_count} room entries.")

if __name__ == "__main__":
    delete_all_rooms()
