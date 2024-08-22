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

router = APIRouter(prefix="/search", tags=["search"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

templates = Jinja2Templates(directory=conf.TEMPLATE_FOLDER)



@router.post("/inn", dependencies=[Depends(check_auth)])
async def client_login(request: Request, inn: str = Form(...), db: Session = Depends(get_db)):
    company = crud.get_company_by_inn(db, inn)
    arbitration = crud.get_arbitration_by_id_company(db, company.id)
    return templates.TemplateResponse("CheckCompany.html",
                                      {"request": request, "company": company, "arbitration": arbitration})