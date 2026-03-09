import os
import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

ca = certifi.where()

client = AsyncIOMotorClient(MONGO_URL, tlsCAFile=ca)

db = client.civic_db


users_collection = db.users
issues_collection = db.issues
admins_collection = db.admins
workers_collection = db.workers
