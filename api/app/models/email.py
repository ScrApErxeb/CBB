from sqlalchemy import Column, String, DateTime, Text
from app.db.session import Base
from datetime import datetime

class Email(Base):
    __tablename__ = "emails"

    id = Column(String, primary_key=True, index=True)  # ID Gmail
    snippet = Column(Text, nullable=False)
    internal_date = Column(DateTime, default=datetime.utcnow())
