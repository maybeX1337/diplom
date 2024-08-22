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

router = APIRouter(prefix="/generator_fake_company", tags=["generator_fake_company"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

templates = Jinja2Templates(directory=conf.TEMPLATE_FOLDER)

@router.get("/company")
async def client_login(request: Request, db: Session = Depends(get_db)):
    data = [
        {
            "id": 1,
            "name": "Medicare Solutions",
            "inn": "399-487-426",
            "address": "028 Lindsey Views\nColeberg, OH 70413",
            "rating": "3.8",
            "industry": "Healthcare",
            "phone": "906.543.3407x622",
            "website": "http://www.reynolds.biz/"
        },
        {
            "id": 2,
            "name": "Precision Manufacturing",
            "inn": "588-191-911",
            "address": "7463 Martinez Fort Apt. 769\nJamesview, IL 06402",
            "rating": "4.1",
            "industry": "Manufacturing",
            "phone": "+1-405-942-1207x62552",
            "website": "https://www.henderson.com/"
        },
        {
            "id": 3,
            "name": "HealthWay Services",
            "inn": "512-098-488",
            "address": "79031 Joshua Ferry Apt. 899\nTeresastad, HI 82445",
            "rating": "2.5",
            "industry": "Healthcare",
            "phone": "+1-309-653-7146x75334",
            "website": "https://www.johnson-washington.com/"
        },
        {
            "id": 4,
            "name": "Retail Masters",
            "inn": "522-523-855",
            "address": "66643 Baker Lodge Suite 384\nEast Christinaberg, MH 11704",
            "rating": "4.8",
            "industry": "Retail",
            "phone": "+1-566-881-3519x12081",
            "website": "https://www.gentry-matthews.biz/"
        },
        {
            "id": 5,
            "name": "Finance Hub",
            "inn": "957-328-245",
            "address": "995 Catherine Trafficway\nLake Jessicaberg, FM 43900",
            "rating": "3.2",
            "industry": "Finance",
            "phone": "(726)736-2271x28686",
            "website": "https://www.parker-wheeler.org/"
        },
        {
            "id": 6,
            "name": "Tech Innovators",
            "inn": "100-341-073",
            "address": "58295 Bonilla Glens\nEast Melissa, AL 71233",
            "rating": "2.9",
            "industry": "IT",
            "phone": "846-420-2741",
            "website": "http://graham-ballard.org/"
        },
        {
            "id": 7,
            "name": "Advanced IT Solutions",
            "inn": "037-089-066",
            "address": "1997 Michelle Street Apt. 660\nLaurenbury, PW 86616",
            "rating": "3.8",
            "industry": "IT",
            "phone": "821.680.8338x36631",
            "website": "https://york-maddox.com/"
        },
        {
            "id": 8,
            "name": "Retail Express",
            "inn": "602-937-029",
            "address": "4397 Marshall Plain\nAdamtown, MS 75960",
            "rating": "2.4",
            "industry": "Retail",
            "phone": "337.461.5347",
            "website": "https://www.powell.biz/"
        },
        {
            "id": 9,
            "name": "Financial Dynamics",
            "inn": "658-461-379",
            "address": "726 Sharon Harbor Suite 479\nBrownmouth, NH 33770",
            "rating": "3.9",
            "industry": "Finance",
            "phone": "+1-261-822-3444x1816",
            "website": "http://mcfarland.com/"
        },
        {
            "id": 10,
            "name": "Healthcare Experts",
            "inn": "338-827-786",
            "address": "247 Robinson Landing Apt. 783\nWeissmouth, HI 24241",
            "rating": "2.7",
            "industry": "Healthcare",
            "phone": "001-567-782-0531x88350",
            "website": "https://strickland.biz/"
        },
        {
            "id": 11,
            "name": "Prime Finance Group",
            "inn": "502-877-834",
            "address": "74468 Tammy Viaduct\nLake Vincentton, MA 08590",
            "rating": "4.7",
            "industry": "Finance",
            "phone": "+1-854-343-1698x0636",
            "website": "https://wilson.com/"
        },
        {
            "id": 12,
            "name": "MedCare Professionals",
            "inn": "498-560-240",
            "address": "1822 Jenkins Villages Apt. 154\nDillontown, NC 04710",
            "rating": "4.6",
            "industry": "Healthcare",
            "phone": "001-389-310-4947x398",
            "website": "http://www.dixon.com/"
        },
        {
            "id": 13,
            "name": "HealthFirst Solutions",
            "inn": "524-974-135",
            "address": "33907 Richard Expressway Apt. 851\nStephaniebury, GU 20872",
            "rating": "4.5",
            "industry": "Healthcare",
            "phone": "(526)253-8078",
            "website": "http://rice.com/"
        },
        {
            "id": 14,
            "name": "Retail Connections",
            "inn": "287-696-195",
            "address": "7410 Jones Vista\nEast Stephenchester, GA 24343",
            "rating": "2.8",
            "industry": "Retail",
            "phone": "869-820-8739",
            "website": "https://johnson.org/"
        },
        {
            "id": 15,
            "name": "Retail World",
            "inn": "246-842-513",
            "address": "8572 Reyes Underpass\nNew Alexandraland, FM 73712",
            "rating": "3.7",
            "industry": "Retail",
            "phone": "+1-464-692-5563x56781",
            "website": "http://brown.com/"
        },
        {
            "id": 16,
            "name": "IT Networks",
            "inn": "695-565-270",
            "address": "54298 Scott Pines\nPeterberg, SC 63579",
            "rating": "2.3",
            "industry": "IT",
            "phone": "2685418358",
            "website": "https://singleton.com/"
        },
        {
            "id": 17,
            "name": "Retail Zone",
            "inn": "972-307-609",
            "address": "885 Reed Mall Suite 956\nEast Karla, WI 40144",
            "rating": "2.5",
            "industry": "Retail",
            "phone": "(841)590-7219",
            "website": "http://stephens.org/"
        },
        {
            "id": 18,
            "name": "ManuTech Solutions",
            "inn": "783-042-270",
            "address": "5678 Marilyn Summit Suite 193\nDavidburgh, MP 73070",
            "rating": "2.4",
            "industry": "Manufacturing",
            "phone": "(412)259-9800x3081",
            "website": "http://mora-shaffer.com/"
        },
        {
            "id": 19,
            "name": "HealthCore Services",
            "inn": "641-063-414",
            "address": "335 Benson Pine\nHarrisland, MO 02090",
            "rating": "2.6",
            "industry": "Healthcare",
            "phone": "5608988964",
            "website": "http://brown.info/"
        },
        {
            "id": 20,
            "name": "Manufacturing Plus",
            "inn": "145-942-838",
            "address": "6782 Elizabeth Mews Suite 629\nVictoriafort, PR 05802",
            "rating": "2.3",
            "industry": "Manufacturing",
            "phone": "001-550-845-3674x5138",
            "website": "https://wright-hernandez.net/"
        },
        {
            "id": 21,
            "name": "MedExperts Group",
            "inn": "385-892-999",
            "address": "0997 Frank Cape\nKevinbury, MO 75707",
            "rating": "4.9",
            "industry": "Healthcare",
            "phone": "545-858-6277x325",
            "website": "https://www.johnson.com/"
        },
        {
            "id": 22,
            "name": "HealthPro Associates",
            "inn": "522-883-704",
            "address": "552 Sandoval Overpass Apt. 974\nBrittanymouth, GA 65660",
            "rating": "2.5",
            "industry": "Healthcare",
            "phone": "001-687-870-0658x4638",
            "website": "https://www.ward.com/"
        },
        {
            "id": 23,
            "name": "ManuWorks",
            "inn": "373-377-989",
            "address": "003 Taylor Drive Suite 163\nLake Cynthia, MO 42558",
            "rating": "3.1",
            "industry": "Manufacturing",
            "phone": "387.643.9815",
            "website": "https://www.cole.com/"
        },
        {
            "id": 24,
            "name": "Healthcare Solutions",
            "inn": "157-650-760",
            "address": "27793 Curtis Skyway Apt. 827\nNorth Matthew, SC 47683",
            "rating": "3.4",
            "industry": "Healthcare",
            "phone": "926.260.2716",
            "website": "http://www.johnson.biz/"
        },
        {
            "id": 25,
            "name": "Retail Dynamics",
            "inn": "075-526-027",
            "address": "621 Cynthia Trafficway Suite 905\nCarterport, CO 36728",
            "rating": "4.2",
            "industry": "Retail",
            "phone": "+1-797-365-9287",
            "website": "http://newman-sanchez.com/"
        }

    ]
    for i in data:
        crud.create_company(db,i.get("inn"), i.get("name"),i.get("address"),i.get("rating"),i.get("industry"),i.get("phone"),i.get("website"))

    return {"answer": "top"}


@router.get("/arbitration")
async def client_login(request: Request, db: Session = Depends(get_db)):
    data = [
        {
            "id": 1,
            "company_id": 1,
            "company_id_partner": 3,
            "total_sum": 43978,
            "short_description": "Treat talk able experience mother happen."
        },
        {
            "id": 2,
            "company_id": 4,
            "company_id_partner": 5,
            "total_sum": 65790,
            "short_description": "Increase efficiency by optimizing retail processes."
        },
        {
            "id": 3,
            "company_id": 7,
            "company_id_partner": 9,
            "total_sum": 89342,
            "short_description": "Integrating IT solutions with financial services."
        },
        {
            "id": 4,
            "company_id": 12,
            "company_id_partner": 21,
            "total_sum": 123456,
            "short_description": "Enhancing healthcare systems through innovation."
        },
        {
            "id": 5,
            "company_id": 15,
            "company_id_partner": 18,
            "total_sum": 76234,
            "short_description": "Collaboration in manufacturing to drive success."
        },
        {
            "id": 6,
            "company_id": 20,
            "company_id_partner": 23,
            "total_sum": 50505,
            "short_description": "Developing new strategies in healthcare."
        },
        {
            "id": 7,
            "company_id": 14,
            "company_id_partner": 25,
            "total_sum": 81000,
            "short_description": "Retail partnerships to enhance customer experience."
        },
        {
            "id": 8,
            "company_id": 2,
            "company_id_partner": 16,
            "total_sum": 47893,
            "short_description": "Advanced IT solutions for retail efficiency."
        },
        {
            "id": 9,
            "company_id": 6,
            "company_id_partner": 11,
            "total_sum": 67450,
            "short_description": "Integrating finance and technology."
        },
        {
            "id": 10,
            "company_id": 8,
            "company_id_partner": 17,
            "total_sum": 90234,
            "short_description": "Boosting retail operations through IT support."
        }
    ]
    for i in data:
        crud.create_arbitration(db, i.get("company_id"), i.get("company_id_partner"), i.get("total_sum"), i.get("short_description"))

    return {"answer": "top"}