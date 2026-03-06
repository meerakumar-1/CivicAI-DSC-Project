from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from database import db

gridfs_bucket = AsyncIOMotorGridFSBucket(db)


async def upload_image(file):

    contents = await file.read()

    file_id = await gridfs_bucket.upload_from_stream(
        file.filename,
        contents,
        metadata={"contentType": file.content_type}
    )

    return file_id