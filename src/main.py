import uvicorn
from fastapi import FastAPI

import sys
from pathlib import Path

from src.api.auth import auth_router
from src.api.hotels import hotels_router
from src.api.rooms import rooms_router


sys.path.append(str(Path(__file__).parent.parent))


app = FastAPI()

app.include_router(auth_router)
app.include_router(hotels_router)
app.include_router(rooms_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
