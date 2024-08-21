from fastapi import FastAPI
from fastapi import APIRouter, Path, Query, Body, Depends, HTTPException, Request, Response, Cookie
from src.routers import client_router, add_router, confirm_router, admin_router, router
from src.database.models import Base
from src.database.database import engine
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from src.config import conf
from fastapi.templating import Jinja2Templates
from src.dependencies import check_auth
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

file = __file__

templates = Jinja2Templates(directory=conf.TEMPLATE_FOLDER)

Base.metadata.create_all(bind=engine)


app.include_router(client_router.router)
app.include_router(add_router.router)
app.include_router(confirm_router.router)
app.include_router(admin_router.router)
app.include_router(router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def client(request: Request):
    access = request.cookies.get("access")
    if access:
        return templates.TemplateResponse("home.html", {"request": request})
    else:
        return templates.TemplateResponse("registration.html",
                                      {"request": request})


@app.get("/confirm_email", dependencies=[Depends(check_auth)])
async def client_login(request: Request):
    return templates.TemplateResponse("confirm_email.html",
                                      {"request": request})


@app.get("/re", dependencies=[Depends(check_auth)])
async def client_login(request: Request):
    return {"request": "reeeee"}


@app.get("/login")
async def client_login(request: Request):
    return templates.TemplateResponse("login.html",
                                      {"request": request})
