from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from src.database.database import get_db
from src import crud
from src.config import conf
from fastapi import APIRouter, Depends, Request, Form
from pydantic import ValidationError
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import qrcode
from fastapi_mail import FastMail, MessageSchema

from src.database import models
from src.database.schemas import DetailsForm
from src.database.database import get_db
from src import crud
from src.config import conf, HOST_PORT

router = APIRouter()
templates = Jinja2Templates(directory=conf.TEMPLATE_FOLDER)



# @router.get("/view_apartment/{apartment_uuid}", response_class=HTMLResponse)
# async def view_apartment(request: Request, apartment_uuid: str, db: Session = Depends(get_db)):
#     apartment = crud.get_apartment_by_uuid(db, apartment_uuid)
#     if not apartment:
#         return templates.TemplateResponse("view_apartment.html", {"request": request, "address": "Apartment not found"})
#         # raise HTTPException(status_code=404, detail="Apartment not found")
#     return templates.TemplateResponse("view_apartment.html", {"request": request, "address": apartment.address})

# @router.post("/view_wishlist", response_class=HTMLResponse)
# async def enter_details_form(request: Request, email: str = Form(...), db: Session = Depends(get_db)):
#     user = get_user_by_email(db, email)
#     apart = []
#     if user:
#         apartment_user = get_apartment_user_by_id(db, user.id)
#         if apartment_user:
#             for i in apartment_user:
#                 apartment = get_apartment_user_by_id_first(db, i.apartment_id)
#                 apart.append(apartment.address)
#
#     return templates.TemplateResponse("view_wishlist.html", {"request": request, "wishlist": apart})


# router.get("/wishlist", response_class=HTMLResponse)
# async def enter_details_form(request: Request):
#     return templates.TemplateResponse("wishlist.html", {"request": request})
