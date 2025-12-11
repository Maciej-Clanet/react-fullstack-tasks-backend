from fastapi import APIRouter
from db import db


task_01_router = APIRouter()


@task_01_router.get("/test")
def test():
    return {"test": "ok"}
