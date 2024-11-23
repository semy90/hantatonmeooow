from sqlalchemy import BigInteger, Boolean, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import AlchemyBaseModel


class BCSModel(AlchemyBaseModel):
    __tablename__ = "bcs"

    name: Mapped[str] = mapped_column(String(200), unique=False, nullable=True)
    status: Mapped[str] = mapped_column(String(200), unique=False, nullable=True)
    priority: Mapped[str] = mapped_column(BigInteger, unique=False, nullable=False)
    department: Mapped[str] = mapped_column(String(200), unique=False, nullable=True)
    organizer: Mapped[str] = mapped_column(String(200), unique=False, nullable=True)
    id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, primary_key=True)