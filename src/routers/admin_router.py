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

router = APIRouter(prefix="/admin", tags=["admin"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

templates = Jinja2Templates(directory=conf.TEMPLATE_FOLDER)


@router.get("/list", dependencies=[Depends(check_auth)])
async def manager_list(request: Request, access: Annotated[str, Cookie()] = None, db: Session = Depends(get_db)):
    if access:
        try:
            payload = jwt.decode(access, str(SECRET_KEY), algorithms=["HS256"])
            client = crud.get_client_by_id(db, payload["id"])
            if client.is_admin != False:
                clients = crud.read_client_list(db)
                return templates.TemplateResponse("admin.html",
                                      {"request": request, "data": clients})

            else:
                return templates.TemplateResponse("home.html",
                                                  {"request": request})
        except:
            return templates.TemplateResponse("home.html",
                                              {"request": request})
    else:
        return templates.TemplateResponse("login.html",
                                          {"request": request})


@router.post("/ban/{client_id}")
async def ban_user(request: Request, response: Response, client_id: int,
                   db: Session = Depends(get_db), access: Annotated[str, Cookie()] = None):
    payload = jwt.decode(access, str(SECRET_KEY), algorithms=["HS256"])
    admin_client = crud.read_client(db, payload["id"])

    if admin_client.is_admin:
        client = crud.ban_client(db, client_id)
        if client:
            return {"message": f"User {client.email} banned successfully"}
    return templates.TemplateResponse("home.html", {"request": request})


@router.post("/delete/{client_id}")
async def delete_user(request: Request, response: Response, client_id: int,
                      db: Session = Depends(get_db), access: Annotated[str, Cookie()] = None):
    payload = jwt.decode(access, str(SECRET_KEY), algorithms=["HS256"])
    admin_client = crud.read_client(db, payload["id"])

    if admin_client.is_admin:
        client = crud.delete_client(db, client_id)
        if client:
            response.delete_cookie("access")
            response.delete_cookie("refresh")
            return {"message": f"User {client.email} deleted successfully"}
    return templates.TemplateResponse("home.html", {"request": request})