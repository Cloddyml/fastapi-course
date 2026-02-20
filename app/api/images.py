import shutil

from fastapi import APIRouter, BackgroundTasks, UploadFile

from app.tasks.tasks import resize_image

router = APIRouter(prefix="/images", tags=["Изображение отелей"])


@router.post("")
def upload_image(file: UploadFile, background_task: BackgroundTasks):
    image_path = f"app/static/images/{file.filename}"
    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)

    # resize_image.delay(image_path)
    background_task.add_task(resize_image, image_path)

    return {"status": "OK"}
