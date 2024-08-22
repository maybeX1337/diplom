import jwt
from fastapi import FastAPI
from fastapi import APIRouter, Path, Query, Body, Depends, HTTPException, Request, Response, Cookie

from src import crud
from src.routers import client_router, add_router, confirm_router, admin_router, router, buy_router, fake_router, \
    serch_router
from src.database.models import Base
from src.database.database import engine
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from src.config import conf
from fastapi.templating import Jinja2Templates
from src.dependencies import check_auth
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
import datetime
from crypt import methods

import jwt
from fastapi import APIRouter, Path, Query, Body, Depends, HTTPException, Response, Cookie, Form, Request
from fastapi_mail import MessageSchema, FastMail
from sqlalchemy.orm import Session
from typing import Annotated
from src import crud
from fastapi.responses import RedirectResponse
from src.database import schemas, models
from src.database.database import get_db
from src.dependencies import check_auth
from passlib.context import CryptContext
from src.config import SECRET_KEY, conf
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_302_FOUND, HTTP_303_SEE_OTHER, HTTP_307_TEMPORARY_REDIRECT

app = FastAPI()

file = __file__

templates = Jinja2Templates(directory=conf.TEMPLATE_FOLDER)

Base.metadata.create_all(bind=engine)


app.include_router(client_router.router)
app.include_router(add_router.router)
app.include_router(confirm_router.router)
app.include_router(admin_router.router)
app.include_router(buy_router.router)
app.include_router(fake_router.router)
app.include_router(serch_router.router)
app.include_router(router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def client(request: Request, db: Session = Depends(get_db)):
    access = request.cookies.get("access")
    subscribe = crud.get_subscribe(db)
    if access:
        try:
            payload = jwt.decode(access, str(SECRET_KEY), algorithms=["HS256"])
            client = crud.read_client(db, payload["id"])
            if client:
                return templates.TemplateResponse("home.html",
                                              {"request": request, "data": True, "subscribe": subscribe})
        except:
            return templates.TemplateResponse("home.html",
                                              {"request": request, "data": False, "subscribe": subscribe})
    else:
        return templates.TemplateResponse("home.html",
                                          {"request": request, "data": False, "subscribe": subscribe})


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
@app.get("/logout")
async def client_login(request: Request):
    return RedirectResponse("/client/logout")

@app.get("/registration")
async def client_login(request: Request):
    return templates.TemplateResponse("registration.html",
                                      {"request": request})

@app.get("/check_company", dependencies=[Depends(check_auth)])
async def client_login(request: Request, db: Session = Depends(get_db), access: Annotated[str, Cookie()] = None):
    if access:
        payload = jwt.decode(access, str(SECRET_KEY), algorithms=["HS256"])

        client = crud.check_client_subscribe(db, payload["id"])
        if client == True:
            response = templates.TemplateResponse("CheckCompany.html",
                                      {"request": request})
            return response
        else:

            response = RedirectResponse("/")
            return response
    else:
        response = RedirectResponse("/login", status_code=HTTP_303_SEE_OTHER)
        return response
