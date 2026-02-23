from fastapi import APIRouter, BackgroundTasks, UploadFile

from app.services.images import ImagesService

router = APIRouter(prefix="/images", tags=["Изображение отелей"])


@router.post("")
def upload_image(file: UploadFile, background_tasks: BackgroundTasks):
    ImagesService().upload_image(file, background_tasks)
    return {"status": "OK"}
