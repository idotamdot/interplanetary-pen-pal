# ======================================
#  AUTHENTICATION SETUP
# ======================================

import streamlit as st
import streamlit_authenticator as stauth
from passlib.context import CryptContext
from database import SessionLocal, User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db, username: str, password: str, email: str):
    hashed_password = get_password_hash(password)
    db_user = User(username=username, hashed_password=hashed_password, email=email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
