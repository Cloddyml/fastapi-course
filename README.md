docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=abcde \
    -e POSTGRES_PASSWORD=abcde \
    -e POSTGRES_DB=booking \
    --network=myNetwork \
    --volume pg-booking-data:/var/lib/postgresql/data \
    -d postgres:16

docker run --name booking_cache \
    -p 7379:6379 \
    --network=myNetwork \
    -d redis:7.4

docker run --name booking_back \
    -p 8000:8000 \
    --network=myNetwork \
    booking_image

docker run --name booking_celery_worker \
    --network=myNetwork \
    booking_image \
    uv run celery --app=app.tasks.celery_app:celery_instance worker -l INFO

docker run --name booking_celery_beat \
    --network=myNetwork \
    booking_image \
    uv run celery --app=app.tasks.celery_app:celery_instance beat -l INFO




docker build -t booking_image


---

docker compose build

docker compose up

docker compose down