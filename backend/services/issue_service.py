import asyncio
from datetime import datetime
from bson import ObjectId

from database import issues_collection
from services.gemini_service import analyze_issue
from utils.mongo_serializer import serialize_doc
from utils.gridfs_service import upload_image


async def create_issue(title, description, department, latitude, longitude, image, user_id):

    analysis_task = analyze_issue(description, department)
    upload_task = upload_image(image)

    analysis_result, image_id = await asyncio.gather(
        analysis_task,
        upload_task
    )

    ai_department = analysis_result.get("department", department)
    priority = analysis_result.get("priority", "medium")
    priority_score = analysis_result.get("priority_score", 50)

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

    result = await issues_collection.insert_one(new_issue)

    return str(result.inserted_id)


async def get_user_issues(user_id):

    issues = await issues_collection.find(
        {"reported_by": ObjectId(user_id)}
    ).to_list(length=25)

    return [serialize_doc(issue) for issue in issues]


async def get_nearby_issues(lat, lng, radius):

    issues = await issues_collection.find({
        "location": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [lng, lat]
                },
                "$maxDistance": radius
            }
        }
    }).to_list(length=25)

    return [serialize_doc(issue) for issue in issues]