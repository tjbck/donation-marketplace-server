from typing import Optional
from fastapi import UploadFile

import uuid
import config

UPLOAD_FOLDER_DIR = config.UPLOAD_FOLDER_DIR

############################
# Save File Handler
############################


async def save_file(file: UploadFile):
    file.filename = f"{uuid.uuid4()}-{file.filename}"
    contents = await file.read()

    # example of how you can save the file
    with open(f"{UPLOAD_FOLDER_DIR}/{file.filename}", "wb") as f:
        f.write(contents)
        f.close()

    if not file:
        return False
    else:
        return file.filename
