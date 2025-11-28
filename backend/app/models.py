from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base


class PPTData(Base):
    __tablename__ = "pptdata"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String(255), nullable=False, index=True)

    # Equivalent to PHP: object (JSON text)
    object = Column(JSONB, nullable=True)   # PostgreSQL JSONB

    # Extra fields for future
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
