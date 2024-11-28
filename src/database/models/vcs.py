from sqlalchemy import BigInteger, Boolean, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import AlchemyBaseModel
class VCSModel(AlchemyBaseModel):
    __tablename__ = "vcs"

    id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, primary_key=True)
    dumped_json: Mapped[str] = mapped_column(String)