import datetime
import jwt
from fastapi import APIRouter, Path, Query, Body, Depends, HTTPException, Response, Cookie, Form, Request
from fastapi_mail import MessageSchema, FastMail
from sqlalchemy.orm import Session
from typing import Annotated
from starlette.status import HTTP_302_FOUND,HTTP_303_SEE_OTHER
from fastapi.responses import RedirectResponse
from src import crud
from src.database import schemas, models
from src.database.database import get_db
from src.dependencies import check_auth
from passlib.context import CryptContext
from src.config import SECRET_KEY, conf
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/confirm", tags=["confirm"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

templates = Jinja2Templates(directory=conf.TEMPLATE_FOLDER)



@router.post("/send_confirmation_code")
async def send_confirmation_code(request: Request, db: Session = Depends(get_db), access: Annotated[str, Cookie()] = None):
    payload = jwt.decode(access, str(SECRET_KEY), algorithms=["HS256"])
    user = crud.get_client_by_id(db, payload["id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    confirmation_code = crud.generate_confirmation_code()
    crud.save_confirmation_code(db, user.id, confirmation_code)

    message = MessageSchema(
        subject="Your Confirmation Code",
        recipients=[user.email],
        body=f"<p>Your confirmation code is: <strong>{confirmation_code}</strong></p>",
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)

    return RedirectResponse("/confirm_email", status_code=HTTP_303_SEE_OTHER)




@router.post("/verify_confirmation_code")
async def verify_confirmation_code(request: Request, code: str = Form(...), db: Session = Depends(get_db), access: Annotated[str, Cookie()] = None):
    payload = jwt.decode(access, str(SECRET_KEY), algorithms=["HS256"])
    user = crud.get_client_by_id(db, payload["id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    is_valid = crud.check_confirmation_code(db, user.id, code)
    if is_valid:
        crud.confirm_email(db, user.id)
        return RedirectResponse("/client/profile", status_code=HTTP_303_SEE_OTHER)
    else:
        raise HTTPException(status_code=400, detail="Invalid confirmation code")