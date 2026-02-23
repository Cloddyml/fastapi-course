import shutil

from fastapi import BackgroundTasks, UploadFile

from app.services.base import BaseService
from app.tasks.tasks import resize_image


class ImagesService(BaseService):
    def upload_image(self, file: UploadFile, background_tasks: BackgroundTasks):
        image_path = f"app/static/images/{file.filename}"
        with open(image_path, "wb+") as new_file:
            shutil.copyfileobj(file.file, new_file)

        # resize_image.delay(image_path)
        background_tasks.add_task(resize_image, image_path)
