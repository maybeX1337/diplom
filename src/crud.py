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

def ban_client(db: Session, client_id: int):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if client:
        client.is_banned = True
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
