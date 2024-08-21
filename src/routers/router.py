from fastapi_mail import MessageSchema, FastMail
from sqlalchemy.orm import Session
from typing import Annotated
from src import crud
from src.database import schemas, models
import datetime
import jwt
from fastapi import APIRouter, Path, Query, Body, Depends, HTTPException, Response, Cookie, Form, Request
from src.database.database import get_db
from src.dependencies import check_auth
from passlib.context import CryptContext
from src.config import SECRET_KEY, conf
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/all", tags=["all"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

templates = Jinja2Templates(directory=conf.TEMPLATE_FOLDER)






@router.get("/log")
async def client_login(request: Request):
    return templates.TemplateResponse("login.html",
                                      {"request": request})