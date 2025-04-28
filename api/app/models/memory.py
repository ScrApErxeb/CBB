from sqlalchemy import Column, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.db.session import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

class Memory(Base):
    __tablename__ = "memories"

    # ID de la mémoire, maintenant en UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # UUID pour id
    
    content = Column(Text, nullable=False)
    tags = Column(String, nullable=True)
    source = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.now())
    
    # source par défaut définie comme 'manual'
    source = Column(String, nullable=False, default="manual")
    
    # user_id maintenant en UUID
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))  # Foreign key avec UUID

    # Relation avec la table User
    user = relationship("User", back_populates="memories")
