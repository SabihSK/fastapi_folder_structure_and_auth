"""Models of Auth"""
from sqlalchemy import Boolean, Column, Enum, Integer, String

from db.db_mixin import Timestamp
from db.db_setup import Base

from .dependency import UserRole


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
    cnic = Column(String(13), unique=True, index=True, nullable=False)
    phone = Column(String(13), index=True, nullable=False)
    password = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=False)
    user_role = Column(Enum(UserRole), nullable=False)
    document_id = Column(String(10))
    property_owner = Column(Boolean, default=False)
