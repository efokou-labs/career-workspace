from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_session, init_db, ping
from app.models import ApplicationRow
from app.queue import enqueue_created


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title="askel", lifespan=lifespan)


class ApplicationIn(BaseModel):
    company: str
    role: str
    status: str = "draft"


class ApplicationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company: str
    role: str
    status: str


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/readyz")
def readyz():
    try:
        ping()
    except Exception:
        return JSONResponse({"status": "not ready"}, status_code=503)
    return {"status": "ready"}


@app.get("/applications", response_model=list[ApplicationOut])
def list_applications(session: Session = Depends(get_session)):
    rows = session.scalars(select(ApplicationRow).order_by(ApplicationRow.id)).all()
    return rows


@app.post("/applications", response_model=ApplicationOut)
def create_application(item: ApplicationIn, session: Session = Depends(get_session)):
    row = ApplicationRow(company=item.company, role=item.role, status=item.status)
    session.add(row)
    session.flush()
    enqueue_created(row.company, row.role, row.status)
    return row
