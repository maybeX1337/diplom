import datetime
import jwt
from fastapi import Request, Response, HTTPException
from sqlalchemy.orm import Session

from src import crud
from src.config import SECRET_KEY, conf
from fastapi.templating import Jinja2Templates

from src.database.database import get_db

templates = Jinja2Templates(directory=conf.TEMPLATE_FOLDER)


async def check_auth(request: Request, response: Response):
    access = request.cookies.get('access')
    refresh = request.cookies.get('refresh')

    if access is None and refresh:
        try:
            payload_refresh = jwt.decode(refresh, str(SECRET_KEY), algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=403, detail="Refresh token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=403, detail="Invalid refresh token")

        payload_access_new = {
            "id": payload_refresh["id"],
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }
        access_new = jwt.encode(payload_access_new, str(SECRET_KEY), algorithm="HS256")

        # Set the new access token in the cookies
        response.set_cookie(key="access", value=access_new, max_age=1800)
        return access_new  # Return the new access token instead of raising it

    elif access is None and refresh is None:
        raise HTTPException(status_code=403, detail="Not authorized, login required")

    elif access:
        try:
            payload = jwt.decode(access, str(SECRET_KEY), algorithms=["HS256"])
            db: Session = next(get_db())
            client = crud.read_client(db, payload["id"])

            if client is None or client.is_banned:
                # Удаление куки и отправка на страницу логина
                response.delete_cookie("access")
                response.delete_cookie("refresh")

                raise HTTPException(status_code=403, detail="Your account has been banned or deleted.")

        except jwt.ExpiredSignatureError:
            return templates.TemplateResponse("login.html", {"request": request, "error": "Token expired"})
        except jwt.InvalidTokenError:
            return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid token"})

    # Optionally return some value or None
    return None
