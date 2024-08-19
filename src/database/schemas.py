from pydantic import BaseModel, EmailStr, constr, validator, StrictStr


class ApartmentCreate(BaseModel):
    address: str


class ApartmentResponse(BaseModel):
    uuid: str
    qr_code_path: str


class ClientConfirm(BaseModel):
    email: EmailStr
    phone: str


class ClientBase(BaseModel):
    email: EmailStr


class ClientCreate(ClientBase):
    password: str


class ClientCreateResponse(BaseModel):
    message: str
    email: EmailStr
    phone: str


class DetailsForm(BaseModel):
    email: EmailStr
    phone: StrictStr

    @validator('phone')
    def validate_phone(cls, v):
        import re
        phone_regex = re.compile(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{11}$')
        if not phone_regex.match(v):
            raise ValueError('Invalid phone number format')
        return v
