import datetime
import jwt
from fastapi import APIRouter, Path, Query, Body, Depends, HTTPException, Response, Cookie, Form, Request
from fastapi_mail import MessageSchema, FastMail
from sqlalchemy.orm import Session
from typing import Annotated
from src import crud
from src.database import schemas, models
from src.database.database import get_db
from src.dependencies import check_auth
from passlib.context import CryptContext
from src.config import SECRET_KEY, conf
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

router = APIRouter(prefix="/add", tags=["add"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

templates = Jinja2Templates(directory=conf.TEMPLATE_FOLDER)




@router.post("/add_phone", dependencies=[Depends(check_auth)])
async def add_phone(request: Request, phone: str = Form(...), access: Annotated[str, Cookie()] = None,
                    db: Session = Depends(get_db)):
    if access:
        try:
            payload = jwt.decode(access, str(SECRET_KEY), algorithms=["HS256"])
            try:
                # Валидация данных формы
                form_data = schemas.DetailsForm(phone=phone)
            except ValidationError as e:
                # Обработка ошибок валидации и отображение на странице
                errors = [err['msg'] for err in e.errors()]
                return templates.TemplateResponse("add_phone.html",
                                                  {"request": request,
                                                   "errors": errors})
            is_phone = crud.get_client_by_phone(db, phone)
            if is_phone == True:
                return templates.TemplateResponse("add_phone.html",
                                                  {"request": request, "errors": "This phone is already registered"})

            client = crud.add_client_phone(db, payload["id"], phone)
            return templates.TemplateResponse("profile.html",
                                              {"request": request, "data": client})
        except:
            return templates.TemplateResponse("login.html",
                                              {"request": request})
    else:
        pass


@router.get("/add_phone", dependencies=[Depends(check_auth)])
async def add_phone_template(request: Request, access: Annotated[str, Cookie()] = None, db: Session = Depends(get_db)):
    if access:
        try:
            payload = jwt.decode(access, str(SECRET_KEY), algorithms=["HS256"])
            client = crud.get_client_by_id(db, payload["id"])
            if client.phone != None:
                return templates.TemplateResponse("profile.html",
                                      {"request": request, "data": client})

            else:
                return templates.TemplateResponse("add_phone.html",
                                                  {"request": request})
        except:
            return templates.TemplateResponse("home.html",
                                              {"request": request})
    else:
        return templates.TemplateResponse("login.html",
                                          {"request": request})
