from fastapi import FastAPI
from fastapi import APIRouter, Path, Query, Body, Depends, HTTPException, Request, Response, Cookie
from src.routers import client_router
from src.database.models import Base
from src.database.database import engine
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from src.config import conf
from fastapi.templating import Jinja2Templates
from src.dependencies import check_auth
from typing import Annotated

app = FastAPI()

file = __file__

templates = Jinja2Templates(directory=conf.TEMPLATE_FOLDER)

Base.metadata.create_all(bind=engine)


app.include_router(client_router.router)



@app.get("/", dependencies=[Depends(check_auth)])
async def client(request: Request):
    access = request.cookies.get("access")
    if access:
        return templates.TemplateResponse("home.html", {"request": request})
    else:
        return templates.TemplateResponse("registration.html",
                                      {"request": request})
