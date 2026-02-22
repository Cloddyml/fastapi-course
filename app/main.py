# import asyncio
import sys
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache

# from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.backends.redis import RedisBackend

# from app.api.dependencies import get_db

sys.path.append(str(Path(__file__).parent.parent))

from app import redis_manager
from app.api.auth import router as router_auth
from app.api.bookings import router as router_bookings
from app.api.facilities import router as router_facilities
from app.api.hotels import router as router_hotels
from app.api.images import router as router_images
from app.api.rooms import router as router_rooms

# print(f"{settings.DB_NAME=}")


# async def send_emails_bookings_today_checkin():
#     async for db in get_db():
#         bookings = await db.bookings.get_bookings_with_today_checkin()
#         print(f"{bookings=}")


# async def run_send_email_regularly():
#     while True:
#         await send_emails_bookings_today_checkin()
#         await asyncio.sleep(5)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # При старте приложения
    # asyncio.create_task(run_send_email_regularly())
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager._redis), prefix="fastapi-cache")
    yield
    # При выключении/перезагрузке приложения
    await redis_manager.close()


# if settings.MODE == "TEST":
#     FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")


app = FastAPI(lifespan=lifespan)

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_facilities)
app.include_router(router_bookings)
app.include_router(router_images)


def main():
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
