from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
from sqlalchemy import Text

class Memory(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    tags = Column(String, nullable=True)
    source = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow())
    source = Column(String, nullable=False, default="manual")  # Enum pas obligatoire en DB
    user_id = Column(Integer, ForeignKey("users.id"))  # 👈 CLE ETRANGERE

    user = relationship("User", back_populates="memories")
