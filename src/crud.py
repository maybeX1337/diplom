from passlib.context import CryptContext
from sqlalchemy.orm import Session
from src.database import models, schemas
from sqlalchemy.orm import Session
import random
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Client
def read_client(db: Session, client_id: int):
    return db.query(models.Client).filter(models.Client.id == client_id).first()


def read_client_list(db: Session):
    return db.query(models.Client).all()


def read_client_by_email(db: Session, client_email: str):
    return db.query(models.Client).filter(models.Client.email == client_email).first()


def create_client(db: Session, email: str, password: str):
    hashed_password = pwd_context.hash(password)
    db_client = models.Client(email=email, password=hashed_password)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def create_client_subscribe(db: Session, client_id: int, subscribe_id: int):
    db_client_subscribe = models.Client_Subscribe(client_id=client_id, subscribe_id=subscribe_id)
    db.add(db_client_subscribe)
    db.commit()
    db.refresh(db_client_subscribe)
    return db_client_subscribe

def update_client(db: Session, email: str, active: bool):
    client_db = db.query(models.Client).filter(models.Client.email == email).first()
    client_db.is_active = active
    db.commit()
    return client_db

def add_client_phone(db: Session, client_id: int, phone: str):
    client_db = db.query(models.Client).filter(models.Client.id == client_id).first()
    client_db.phone = phone
    db.commit()
    return client_db


def get_client_by_email(db: Session, email: str):
    return db.query(models.Client).filter(models.Client.email == email).first()


def get_client_by_id(db: Session, id: int):
    return db.query(models.Client).filter(models.Client.id == id).first()


def get_subscribe_by_id(db: Session, id: int):
    return db.query(models.Subscribe).filter(models.Subscribe.id == id).first()

def get_subscribe(db: Session):
    return db.query(models.Subscribe).all()

def ban_client(db: Session, client_id: int):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if client:
        client.is_banned = True
        db.commit()
    return client
def unban_client(db: Session, client_id: int):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if client:
        client.is_banned = False
        db.commit()
    return client

def delete_client(db: Session, client_id: int):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if client:
        db.delete(client)
        db.commit()
    return client



def generate_confirmation_code() -> str:
    return str(random.randint(100000, 999999))

def save_confirmation_code(db: Session, user_id: int, code: str):
    confirmation = db.query(models.EmailConfirmation).filter(models.EmailConfirmation.user_id == user_id).first()
    if confirmation:
        confirmation.confirmation_code = code
    else:
        confirmation = models.EmailConfirmation(user_id=user_id, confirmation_code=code)
        db.add(confirmation)
    db.commit()

def check_confirmation_code(db: Session, user_id: int, code: str) -> bool:
    confirmation = db.query(models.EmailConfirmation).filter(models.EmailConfirmation.user_id == user_id, models.EmailConfirmation.confirmation_code == code).first()
    return confirmation is not None

def confirm_email(db: Session, user_id: int):
    user = db.query(models.Client).filter(models.Client.id == user_id).first()
    if user:
        user.is_confirmed = True
        db.commit()

def get_client_by_phone(db: Session, phone: str):
    client = db.query(models.Client).filter(models.Client.phone == phone).first()
    if client:
        return True
    else:
        return False

def check_client_subscribe(db: Session, id: int):
    client = db.query(models.Client_Subscribe).filter(models.Client_Subscribe.client_id == id).first()
    if client:
        return True
    else:
        return False


def create_company(db: Session, inn: str, name: str, address: str, rating: str, industry: str, phone: str, website: str):
    db_company = models.Company(inn=inn, name=name, address=address, rating=rating, industry=industry, phone=phone, website=website)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def create_arbitration(db: Session, company_id: int, company_id_partner: int, total_sum: int, short_description: str):
    db_arbitration = models.Arbitration(company_id=company_id, company_id_partner=company_id_partner, total_sum=total_sum, short_description=short_description)
    db.add(db_arbitration)
    db.commit()
    db.refresh(db_arbitration)
    return db_arbitration


def get_company_by_inn(db: Session, inn: str):
    return db.query(models.Company).filter(models.Company.inn == inn).first()

def get_company_by_id(db: Session, id: int):
    return db.query(models.Company).filter(models.Company.id == id).first()

def get_arbitration_by_id_company(db: Session, id: int):
    return db.query(models.Arbitration).filter(models.Arbitration.company_id == id).all()

def get_arbitration_by_id_company_partner(db: Session, id: int):
    return db.query(models.Arbitration).filter(models.Arbitration.company_id_partner == id).all()


def get_companies_by_industry(db: Session, industry: str):
    return db.query(models.Company).filter(models.Company.industry == industry).all()