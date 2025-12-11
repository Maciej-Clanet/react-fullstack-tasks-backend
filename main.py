from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# routes
from tasks.example.routes import example_router
from tasks.task_01.routes import task_01_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(example_router, prefix="/example", tags=["Examples"])
app.include_router(task_01_router, prefix="/task_01", tags=["Task 01"])


@app.get("/")
def read_root():
    return {"Hello": "World"}
