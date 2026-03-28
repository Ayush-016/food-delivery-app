import uuid
from fastapi import HTTPException

ALLOWED = ["image/jpeg", "image/png"]

def save_image(image):
    if image.content_type not in ALLOWED:
        raise HTTPException(400, "Invalid file type")

    filename = f"{uuid.uuid4()}.jpg"
    path = f"uploads/{filename}"

    with open(path, "wb") as f:
        f.write(image.file.read())

    return path