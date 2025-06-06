from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.db.session import Base
import uuid
from datetime import datetime

class LocalDocument(Base):
    __tablename__ = "local_documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    filename = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
