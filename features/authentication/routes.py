"""Authentication routes for api."""

from __future__ import annotations

# from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from configuration import constants
from db.db_setup import get_db
from features.authentication.dependency import (
    check_if_user_exist,
    check_password,
    create_user,
    get_user_by_cnic,
)
from features.authentication.schemas import Login, Register

userAuth = APIRouter()


@userAuth.post("/user/register")
async def register_user(
    user: Register,
    db: Session = Depends(get_db),
) -> dict:
    """Register the user.

    Args:
        user (Login): Schema of user
        db (Session, optional): Defaults to Depends(get_db).

    Returns:
        dict[str, str]: will return info from db.
    """

    if check_if_user_exist(db=db, user=user):
        raise HTTPException(
            status_code=400,
            detail={
                "status": False,
                "message": constants.ALREADY_REGISTERED,
            },
        )

    return create_user(db=db, user=user)


@userAuth.post("/user/signin")
async def signin_user(
    user: Login,
    db: Session = Depends(get_db),
) -> dict:
    """Sign the user.

    Returns:
        User: Will return user info.
    """
    if not (db_user := get_user_by_cnic(db=db, cnic=user.cnic)):
        raise HTTPException(
            status_code=404,
            detail={
                "status": False,
                "message": constants.USER_NOT_FOUND,
            },
        )
    return check_password(password=user.password, user=db_user)
