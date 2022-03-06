from fastapi import FastAPI
from .routers import nasdaq
app = FastAPI()


app.include_router(
    nasdaq.router,
    prefix="/nasdaq",
    tags=["nasdaq"]
)