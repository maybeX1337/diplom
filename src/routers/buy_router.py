import datetime
from http.client import responses

import jwt
from fastapi import APIRouter, Path, Query, Body, Depends, HTTPException, Response, Cookie, Form, Request
from fastapi_mail import MessageSchema, FastMail
from sqlalchemy.orm import Session
from typing import Annotated

from fastapi.responses import RedirectResponse
from starlette.status import HTTP_302_FOUND,HTTP_303_SEE_OTHER
from src import crud
from src.database import schemas, models
from src.database.database import get_db
from src.dependencies import check_auth
from passlib.context import CryptContext
from src.config import SECRET_KEY, conf
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

router = APIRouter(prefix="/buy", tags=["buy"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

templates = Jinja2Templates(directory=conf.TEMPLATE_FOLDER)




@router.post("/subscribe/{id}", dependencies=[Depends(check_auth)])
async def add_phone_template(request: Request, id: int, access: Annotated[str, Cookie()] = None, db: Session = Depends(get_db)):
    if access:
        subscribe = crud.get_subscribe_by_id(db, id)
        payload = jwt.decode(access, str(SECRET_KEY), algorithms=["HS256"])
        if subscribe:
            client = crud.check_client_subscribe(db, payload["id"])
            if client == True:
                response = RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)
                return response
            else:
                w = crud.create_client_subscribe(db, payload["id"], subscribe.id)
                response = RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)
                return response
        else:
            response = RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)
            return response
    else:
        response = RedirectResponse("/login", status_code=HTTP_303_SEE_OTHER)
        return response


@router.get("/subscribe/{id}", dependencies=[Depends(check_auth)])
async def add_phone_template(request: Request, id: int, access: Annotated[str, Cookie()] = None, db: Session = Depends(get_db)):
    if access:
        subscribe = crud.get_subscribe_by_id(db, id)
        payload = jwt.decode(access, str(SECRET_KEY), algorithms=["HS256"])
        if subscribe:
            client = crud.check_client_subscribe(db, payload["id"])
            if client == True:
                response = RedirectResponse("/")
                return response
            else:
                response = templates.TemplateResponse("paymant.html",
                                                      {"request": request, "subscribe": subscribe})
                return response
        else:
            response = RedirectResponse("/")
            return response
    else:
        response = RedirectResponse("/login")
        return response