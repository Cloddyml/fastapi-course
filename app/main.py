import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI

sys.path.append(str(Path(__file__).parent.parent))

from app.api.auth import router as router_auth
from app.api.bookings import router as router_bookings
from app.api.facilities import router as router_facilities
from app.api.hotels import router as router_hotels
from app.api.rooms import router as router_rooms

# print(f"{settings.DB_NAME=}")

app = FastAPI()

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)


def main():
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
