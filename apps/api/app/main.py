from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="career-workspace")


class Application(BaseModel):
    company: str
    role: str
    status: str = "draft"


STORE: list[Application] = []


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/readyz")
def readyz():
    return {"status": "ready"}


@app.get("/applications")
def list_applications():
    return STORE


@app.post("/applications")
def create_application(item: Application):
    STORE.append(item)
    return item
