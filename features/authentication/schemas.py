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


class OTPverification(BaseModel):
    """User OTPverification model.

    Args:
        BaseModel (pydantic): pydantic type model
    """

    email: EmailStr
    otp: str

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


class ForgotPassword(BaseModel):
    """User ForgotPassword model.

    Args:
        BaseModel (pydantic): pydantic type model
    """

    email: EmailStr

    class Config:
        from_attributes = True


class ResetUserPassword(BaseModel):
    """User ResetUserPassword model.

    Args:
        BaseModel (pydantic): pydantic type model
    """

    email: EmailStr
    password: str

    class Config:
        from_attributes = True
