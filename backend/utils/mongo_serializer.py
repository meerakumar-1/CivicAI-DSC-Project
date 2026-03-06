from bson import ObjectId
from datetime import datetime

def serialize_doc(doc):

    if not doc:
        return doc

<<<<<<< HEAD
    doc["_id"] = str(doc["_id"])
=======
    if "_id" in doc and isinstance(doc["_id"], ObjectId):
        doc["_id"] = str(doc["_id"])
>>>>>>> 5d161d7 (Migrated from  pymongo to motor client and successfully merged with suhas's backend-dev branch)

    if "reported_by" in doc and isinstance(doc["reported_by"], ObjectId):
        doc["reported_by"] = str(doc["reported_by"])

    if "image_id" in doc and isinstance(doc["image_id"], ObjectId):
        doc["image_id"] = str(doc["image_id"])

    if "created_at" in doc and isinstance(doc["created_at"], datetime):
        doc["created_at"] = doc["created_at"].isoformat()

    return doc