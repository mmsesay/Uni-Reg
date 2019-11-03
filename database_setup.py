#!/usr/bin/python
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from itsdangerous import(
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature,
    SignatureExpired)

Base = declarative_base()
    
# Admin Class
class User(Base, UserMixin):
    """This is the Admin schema class"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    account_type = Column(String(100), nullable=False)
    initial_login = Column(Boolean(),  default=False)
    hash_password = Column(String(64))

    # constructor
    def __init__(self, username,email,password,account_type,initial_login):
        self.username = username
        self.email = email
        self.account_type = account_type
        self.hash_password = generate_password_hash(password)

    # verify password function
    def verify_password(self, password):
        return check_password_hash(self.hash_password, password)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id': self.id,
           'username': self.username
       }


# Contract Class
class Contract(Base):
    """This is the Contract schema class"""
    __tablename__ = "contract"

    id = Column(Integer, primary_key=True)
    company_name = Column(String(250), nullable=False)
    company_address = Column(String(250), nullable=False)
    company_mobile = Column(String(250), nullable=False)
    contract_type = Column(String(250), nullable=False)
    contract_document = Column(String(250), nullable=True)
    signed_date = Column(String(250), nullable=False)
    expiration_date = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)

    # constructor
    # def __init__(self, company_name,company_address,company_mobile,contract_type,
    #             contract_document,signed_date,expiration_date,user_id):
    #     self.company_name = company_name
    #     self.company_address = company_address
    #     self.company_mobile = company_mobile
    #     self.contract_type = contract_type
    #     self.contract_document = contract_document
    #     self.signed_date = signed_date
    #     self.expiration_date = expiration_date
    #     self.user_id = user_id

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
            'id': self.id,
            'company_name': self.company_name,
            'company_address': self.company_address,
            'company_mobile': self.company_mobile,
            'contract_type': self.contract_type,
            'signed_date': self.signed_date,
            'expiration_date': self.expiration_date
       }
   

# connection engine
engine = create_engine('sqlite:///orange_contract.db?check_same_thread=False')
 
#  binding the engine
Base.metadata.create_all(engine)
