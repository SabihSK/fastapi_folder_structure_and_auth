"""Models of Auth"""
from sqlalchemy import Boolean, Column, Enum, Integer, String

from db.db_mixin import Timestamp
from db.db_setup import Base
from utilities.enums import UserRole


class UserModel(Timestamp, Base):
    """User Model class.

    Args:
        Base (declarative_base)
        Timestamp (Datetime)
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(13), index=True)
    password = Column(String(100), nullable=False)
    is_verify = Column(Boolean, default=False)
    user_role = Column(Enum(UserRole), nullable=False)
    otp = Column(String(6))
