<<<<<<< HEAD
from main import db
import gridfs
=======
import os
import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
>>>>>>> 5d161d7 (Migrated from  pymongo to motor client and successfully merged with suhas's backend-dev branch)

users_collection = db.users
issues_collection = db.issues
admins_collection = db.admins
workers_collection = db.workers
fs = gridfs.GridFS(db)

<<<<<<< HEAD
=======
MONGO_URL = os.getenv("MONGO_URL")

ca = certifi.where()

client = AsyncIOMotorClient(MONGO_URL, tlsCAFile=ca)

db = client.civic_db


users_collection = db.users
issues_collection = db.issues
admins_collection = db.admins
workers_collection = db.workers
>>>>>>> 5d161d7 (Migrated from  pymongo to motor client and successfully merged with suhas's backend-dev branch)
