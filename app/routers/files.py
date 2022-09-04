from fastapi import APIRouter, File, UploadFile
from typing import Optional

import uuid
import config

UPLOAD_FOLDER_DIR = config.UPLOAD_FOLDER_DIR

router = APIRouter()

###############################
# Upload File
###############################


@router.post("/files/upload", tags=["files"])
async def upload_file(file: Optional[UploadFile] = File(None)):
    file.filename = f"{uuid.uuid4()}-{file.filename}"
    contents = await file.read()

    # example of how you can save the file
    with open(f"{UPLOAD_FOLDER_DIR}/{file.filename}", "wb") as f:
        f.write(contents)
        f.close()

    if not file:
        return {"error": "No file sent"}
    else:
        return {
            "status": True,
            "src": f'/static/{file.filename}',
            "filename": file.filename,
            "filetype": file.content_type
        }
