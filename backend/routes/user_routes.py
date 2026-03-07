from fastapi import APIRouter, Depends, UploadFile, File, Form
from services.issue_service import create_issue
from utils.auth_dependency import get_current_user
from services.issue_service import get_user_issues,get_nearby_issues
from fastapi.responses import StreamingResponse
from utils.gridfs_service import gridfs_bucket
from bson import ObjectId
from utils.mongo_serializer import serialize_doc
from database import issues_collection

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/report")
async def report_issue(
    title: str = Form(...),
    description: str = Form(...),
    department: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    image: UploadFile = File(...),
    user=Depends(get_current_user)
):

    issue_id = await create_issue(
        title,
        description,
        department,
        latitude,
        longitude,
        image,
        user["_id"]
    )

    return {
        "message": "Issue reported successfully",
        "issue_id": issue_id
    }

@router.get("/my-issues")
async def my_issues(user=Depends(get_current_user)):
    issues = await get_user_issues(user["_id"])
    return issues


@router.get("/nearby")
async def nearby_issues(lat: float, lng: float, radius: int = 1000):
    issues = await get_nearby_issues(lat, lng, radius)
    return [serialize_doc(issue) for issue in issues]

@router.get("/issue/{issue_id}")
async def get_issue(issue_id: str):
    issue =await issues_collection.find_one({"_id": ObjectId(issue_id)})
    return [serialize_doc(issue)]



@router.get("/image/{image_id}")
async def get_image(image_id: str):

    grid_out = await gridfs_bucket.open_download_stream(ObjectId(image_id))

    return StreamingResponse(
        grid_out,
        media_type="image/jpeg"
    )
