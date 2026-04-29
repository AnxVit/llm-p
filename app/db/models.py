from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum, DateTime, func, ForeignKey, Text

from datetime import datetime

from app.db.base import Base

MESSAGE_ROLE_USER = "user"
MESSAGE_ROLE_ASSISTANT = "assistant"

ROLE_USER = "user"

USERS_TABLE = "users"
CHAT_MESSAGE_TABLE = "chat_message"

class Users(Base):
    __tablename__ = USERS_TABLE

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(Enum(ROLE_USER, 
        name="user_role",
        create_type=True
    ), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    messages: Mapped["ChatMessage"] = relationship(
        back_populates="users",
        cascade="all, delete-orphan"
    )

class ChatMessage(Base):
    __tablename__ = CHAT_MESSAGE_TABLE

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(USERS_TABLE + ".id", ondelete="CASCADE"))
    role: Mapped[str] = mapped_column(Enum(MESSAGE_ROLE_USER, MESSAGE_ROLE_ASSISTANT, 
        name="message_role",
        create_type=True
    ))
    content: Mapped[Text] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    users: Mapped["Users"] = relationship(back_populates="messages")