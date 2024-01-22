"""Dependency of Auth"""

import random
import string

from sqlalchemy import or_
from sqlalchemy.orm import Session

from configuration import constants
from features.authentication.schemas import Login, Register
from utilities.email.main_email import gmail_html_email_sender
from utilities.enums import UserRole, EmailTemplate
from utilities.hashed_password import get_hashed_password, verify_password

from .models import UserModel


def get_user_by_cnic(db: Session, cnic: str) -> UserModel:
    return db.query(UserModel).filter(UserModel.cnic == cnic).first()


def check_if_user_exist(db: Session, user: Register) -> UserModel:
    return (
        db.query(UserModel)
        .filter(
            or_(
                UserModel.email == user.email,
                UserModel.cnic == user.cnic,
            ),
        )
        .first()
    )


def check_password(password: str, user: Login) -> dict[str, object]:
    if not verify_password(password, user.password):
        return {
            "status": False,
            "message": constants.USER_NOT_FOUND,
        }
    else:
        return {
            "status": True,
            "message": constants.USER_LOGIN,
            "data": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "cnic": user.cnic,
                "phone": user.phone,
                "is_active": user.is_active,
                "user_role": user.user_role,
                "document_id": user.document_id,
                "property_owner": user.property_owner,
            },
        }


def get_users(db: Session, skip: int = 0, limit: int = 100) -> UserModel:
    return db.query(UserModel).offset(skip).limit(limit).all()


def create_user(db: Session, user: Register) -> dict[str, object]:
    try:
        otp = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        db_user = UserModel(
            full_name=user.full_name,
            email=user.email,
            cnic=user.cnic,
            phone=user.phone,
            password=get_hashed_password(user.password),
            user_role=UserRole.USER,
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        gmail_html_email_sender(
            user.full_name,
            otp,
            user.email,
            EmailTemplate.SIGNUP
        )

        return {
            "status": True,
            "message": constants.USER_REGISTERED,
            "data": {
                "id": db_user.id,
                "full_name": db_user.full_name,
                "email": db_user.email,
                "cnic": db_user.cnic,
                "phone": db_user.phone,
                "is_active": db_user.is_active,
                "user_role": db_user.user_role,
                "document_id": db_user.document_id,
                "property_owner": db_user.property_owner,
            },
        }

    except KeyError:
        return {
            "status": False,
            "message": "error",
        }
