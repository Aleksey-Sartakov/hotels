import shutil

from fastapi import APIRouter, UploadFile

from src.tasks.tasks import resize_image


images_router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@images_router.post("")
async def upload_image(file: UploadFile):
    output_folder = f"src/static/images/{file.filename}"
    with open(output_folder, "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)

    resize_image(output_folder)
