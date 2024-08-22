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
from starlette.status import HTTP_302_FOUND,HTTP_303_SEE_OTHER

router = APIRouter(prefix="/client", tags=["client"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

templates = Jinja2Templates(directory=conf.TEMPLATE_FOLDER)








@router.post("/registration")
async def registration(request: Request, email: str = Form(...), password: str = Form(...),
                       db: Session = Depends(get_db)):
    db_client = crud.read_client_by_email(db, client_email=email)
    if db_client:
        return templates.TemplateResponse("registration.html",
                                          {"request": request, "error": "Client with this email already registered"})
        # raise HTTPException(status_code=400, detail="Client with this email already registered")
    crud.create_client(db=db, email=email, password=password)
    return RedirectResponse("/login", status_code=HTTP_303_SEE_OTHER)


@router.post("/login")
async def login(request: Request, response: Response, email: str = Form(...), password: str = Form(...),
                db: Session = Depends(get_db)):
    db_client = crud.read_client_by_email(db, email)
    if db_client is None or pwd_context.verify(password, db_client.password) == False:
        return templates.TemplateResponse("login.html",
                                          {"request": request, "error": "Incorrect email or password"})
        # raise HTTPException(status_code=400, detail="Incorrect email or password")

    crud.update_client(db, email=email, active=True)

    # Create a payload with an expiration time
    payload_access = {
        "id": db_client.id,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    payload_refresh = {
        "id": db_client.id,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30)
    }

    # Encode the JWT
    access = jwt.encode(payload_access, str(SECRET_KEY), algorithm="HS256")
    refresh = jwt.encode(payload_refresh, str(SECRET_KEY), algorithm="HS256")
    response = RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)
    response.set_cookie(key="access", value=access, httponly=True, max_age=1800)
    response.set_cookie(key="refresh", value=refresh, httponly=True, max_age=2592000)
    return response


@router.post("/logout")
async def logout(response: Response, access: Annotated[str, Cookie()] = None, refresh: Annotated[str, Cookie()] = None,
                 db: Session = Depends(get_db)):
    payload = jwt.decode(access, str(SECRET_KEY), algorithms=["HS256"])
    client = crud.read_client(db, payload["id"])
    crud.update_client(db, client.email, False)
    response = RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)
    response.delete_cookie("access")
    response.delete_cookie("refresh")
    return response


@router.get("/profile", dependencies=[Depends(check_auth)])
async def profile(request: Request, response: Response, access: Annotated[str, Cookie()] = None,
                  refresh: Annotated[str, Cookie()] = None,
                  db: Session = Depends(get_db)):
    if access:
        try:
            payload = jwt.decode(access, str(SECRET_KEY), algorithms=["HS256"])
            client = crud.read_client(db, payload["id"])
            return templates.TemplateResponse("profile.html",
                                              {"request": request, "data": client})
        except:
            return RedirectResponse("/login")
    else:
        pass






