from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(length=200))
    hashed_assword: Mapped[str] = mapped_column(String(length=200))
