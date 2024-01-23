"""Dependency of Auth"""

import random
import string
from datetime import datetime

from fastapi import HTTPException

# from sqlalchemy import or_
from sqlalchemy.orm import Session

from configuration import constants
from features.authentication.schemas import (
    ForgotPassword,
    OTPverification,
    Register,
    ResetUserPassword,
)
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
        raise HTTPException(
            status_code=401,
            detail={
                "status": False,
                "message": constants.INVALID_USER,
            },
        )

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
        return HTTPException(
            status_code=400,
            detail={
                "status": False,
                "message": constants.SOMETHING_WRONG,
            },
        )


def user_verification(db: Session, user: OTPverification, db_user: UserModel) -> dict:
    try:
        if user.otp != db_user.otp:
            raise HTTPException(
                status_code=401,
                detail={
                    "status": False,
                    "message": constants.OTP_NOT_MATCH,
                },
            )
        db.query(UserModel).filter_by(email=user.email).update(
            {UserModel.is_verify: True, UserModel.updated_at: datetime.utcnow()}
        )
        db.commit()

        return {
            "status": True,
            "message": constants.USER_VERIFY,
            "data": {
                "id": db_user.id,
                "full_name": db_user.full_name,
                "email": db_user.email,
                "phone": db_user.phone,
                "user_role": db_user.user_role,
            },
        }

    except KeyError:
        return HTTPException(
            status_code=400,
            detail={
                "status": False,
                "message": constants.SOMETHING_WRONG,
            },
        )


def forgot_password_email(
    db: Session, user: ForgotPassword, db_user: UserModel
) -> dict:
    try:
        otp = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

        db.query(UserModel).filter_by(email=user.email).update(
            {UserModel.otp: otp, UserModel.updated_at: datetime.utcnow()}
        )
        db.commit()

        gmail_html_email_sender(
            db_user.full_name, otp, db_user.email, EmailTemplate.FORGET_PASS.value
        )

        return {
            "status": True,
            "message": constants.OTP_SEND,
        }

    except KeyError:
        return HTTPException(
            status_code=400,
            detail={
                "status": False,
                "message": constants.SOMETHING_WRONG,
            },
        )


def reset_password(db: Session, user: ResetUserPassword, db_user: UserModel) -> dict:
    try:
        db.query(UserModel).filter_by(email=user.email).update(
            {
                UserModel.password: get_hashed_password(user.password),
                UserModel.updated_at: datetime.utcnow(),
            }
        )
        db.commit()

        return {
            "status": True,
            "message": constants.PASSWORD_CHANGE,
            "data": {
                "id": db_user.id,
                "full_name": db_user.full_name,
                "email": db_user.email,
                "phone": db_user.phone,
                "user_role": db_user.user_role,
            },
        }

    except KeyError:
        return HTTPException(
            status_code=400,
            detail={
                "status": False,
                "message": constants.SOMETHING_WRONG,
            },
        )
