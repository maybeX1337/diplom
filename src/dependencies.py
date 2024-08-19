import datetime
import jwt
from fastapi import Request, Response, HTTPException
from src.config import SECRET_KEY, conf
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory=conf.TEMPLATE_FOLDER)


async def check_auth(request: Request, response: Response):
    access = request.cookies.get('access')
    refresh = request.cookies.get('refresh')

    if access is None:
        try:
            payload_refresh = jwt.decode(refresh, SECRET_KEY, algorithms=["HS256"])
            payload_access_new = {
                "id": payload_refresh["id"],
                "iat": datetime.datetime.utcnow(),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }
            access_new = jwt.encode(payload_access_new, SECRET_KEY, algorithm="HS256")
            response.set_cookie(key="access", value=access_new, max_age=1800)
        except:
            return templates.TemplateResponse("registration.html",
                                              {"request": request})
            #raise HTTPException(status_code=400, detail="None authorized, issue refresh and access token")
    else:
        pass
