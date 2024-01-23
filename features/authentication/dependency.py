"""Dependency of Auth"""

import random
import string

# from sqlalchemy import or_
from sqlalchemy.orm import Session

from configuration import constants
from features.authentication.schemas import Register
from utilities.email.main_email import gmail_html_email_sender
from utilities.enums import EmailTemplate, UserRole
from utilities.hashed_password import get_hashed_password, verify_password

from .models import UserModel


def get_user_by_email(db: Session, email: str) -> UserModel:
    return db.query(UserModel).filter(UserModel.email == email).first()


def check_if_user_exist(db: Session, user: Register) -> UserModel:
    return (
        db.query(UserModel)
        .filter(
            UserModel.email == user.email,
        )
        .first()
    )


def check_password(password: str, user: UserModel) -> dict:
    if not verify_password(password, user.password):
        return {
            "status": False,
            "message": constants.USER_NOT_FOUND,
        }

    return {
        "status": True,
        "message": constants.USER_LOGIN,
        "data": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "phone": user.phone,
            "user_role": user.user_role,
        },
    }


def get_users(db: Session, skip: int = 0, limit: int = 100) -> UserModel:
    return db.query(UserModel).offset(skip).limit(limit).all()


def create_user(db: Session, user: Register) -> dict:
    try:
        otp = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        db_user = UserModel(
            full_name=user.full_name,
            email=user.email,
            phone=user.phone,
            password=get_hashed_password(user.password),
            user_role=UserRole.USER,
            otp=otp,
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        gmail_html_email_sender(
            user.full_name, otp, user.email, EmailTemplate.REGISTER.value
        )

        return {
            "status": True,
            "message": constants.USER_REGISTERED,
            "data": {
                "id": db_user.id,
                "full_name": db_user.full_name,
                "email": db_user.email,
                "phone": db_user.phone,
                "user_role": db_user.user_role,
            },
        }

    except KeyError:
        return {
            "status": False,
            "message": "error",
        }
