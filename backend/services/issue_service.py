import asyncio
import json
from datetime import datetime

import pymongo
from bson import ObjectId
from database import issues_collection
from services.gemini_service import analyze_issue
from utils.mongo_serializer import serialize_doc
<<<<<<< HEAD

issues_collection = db.issues_collection
fs = db.fs
=======
from utils.gridfs_service import upload_image
>>>>>>> 5d161d7 (Migrated from  pymongo to motor client and successfully merged with suhas's backend-dev branch)


async def create_issue(title, description, department, latitude, longitude, image, user_id):
    analysis_task = analyze_issue(description)
    upload_task = upload_image(image)

    analysis_result, image_id = await asyncio.gather(
        analysis_task,
        upload_task
    )
    try:
        ai_data = json.loads(analysis_result)
        ai_department = ai_data.get("department", department)
        priority = ai_data.get("priority", "medium")
        priority_score = ai_data.get("priority_score", 50)
    except:
        ai_department = department
        priority = "medium"
        priority_score = 50

    new_issue = {
        "title": title,
        "description": description,

        "department": department,
        "ai_department": ai_department,

        "priority": priority,
        "priority_score": priority_score,

        "reported_by": ObjectId(user_id),

        "status": "raised",

        "image_id": image_id,

        "location": {
            "type": "Point",
            "coordinates": [longitude, latitude]
        },

        "assigned_worker": None,

        "created_at": datetime.utcnow(),
        "resolved_at": None
    }

    result =await issues_collection.insert_one(new_issue)

    return str(result.inserted_id)

async def get_user_issues(user_id):

<<<<<<< HEAD
    issues = list(
        issues_collection.find(
            {"reported_by": ObjectId(user_id)}
        ).sort("created_at", -1)
    )

    return [serialize_doc(issue) for issue in issues]
=======
    issues = await issues_collection.find(
        {"reported_by": ObjectId(user_id)}
    ).to_list(length=100)

    return [serialize_doc(issue) for issue in issues]

async def get_nearby_issues(lat, lng, radius):
>>>>>>> 5d161d7 (Migrated from  pymongo to motor client and successfully merged with suhas's backend-dev branch)

    issues = await issues_collection.find({
        "location": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [lng, lat]
                },
                "$maxDistance": radius
            }
<<<<<<< HEAD
        }).limit(25)
    )
=======
        }
    }).to_list(length=50)
>>>>>>> 5d161d7 (Migrated from  pymongo to motor client and successfully merged with suhas's backend-dev branch)

    return [serialize_doc(issue) for issue in issues]