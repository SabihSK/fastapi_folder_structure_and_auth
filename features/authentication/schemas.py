"""Pydentic give base model for schema"""
from pydantic import BaseModel, EmailStr


class Register(BaseModel):
    """User Register model.

    Args:
        BaseModel (pydantic): pydantic type model
    """

    full_name: str
    email: EmailStr
    phone: str
    password: str

    class Config:
        from_attributes = True


class Login(BaseModel):
    """User Login model.

    Args:
        BaseModel (pydantic): pydantic type model
    """

    email: EmailStr
    password: str

    class Config:
        from_attributes = True
