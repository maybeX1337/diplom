import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def fls():
    return False


def nll():
    return None


class Apartment(Base):
    __tablename__ = "apartment"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    address = Column(String)
    test = Column(String)

class Subscribe(Base):
    __tablename__ = "subscribe"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    price = Column(Integer, nullable=False)


class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    inn = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=False)
    rating = Column(String, nullable=False)
    industry = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    website = Column(String, nullable=False)

class Arbitration(Base):
    __tablename__ = "arbitration"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey('company.id'), primary_key=True)
    company_id_partner = Column(Integer, ForeignKey('company.id'), primary_key=True)
    total_sum = Column(Integer, nullable=False)
    short_description = Column(String, nullable=False)

class Client_Subscribe(Base):
    __tablename__ = "client_subscribe"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('client.id'), primary_key=True)
    subscribe_id = Column(Integer, ForeignKey('subscribe.id'), primary_key=True)



class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=True, default=lambda: nll())
    is_admin = Column(Boolean, nullable=True, default=lambda: fls())
    is_active = Column(Boolean, default=True)
    is_banned = Column(Boolean, default=False)
    is_confirmed = Column(Boolean, default=False)

    email_confirmation = relationship("EmailConfirmation", back_populates="client", uselist=False)


class ApartmentClient(Base):
    __tablename__ = "apartment_client"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    apartment_id = Column(Integer, ForeignKey('apartment.id'), primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id'), primary_key=True)
    confirmed = Column(Boolean, default=lambda: fls())


class EmailConfirmation(Base):
    __tablename__ = "email_confirmations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('client.id'))
    confirmation_code = Column(String, nullable=False)

    client = relationship("Client", back_populates="email_confirmation")