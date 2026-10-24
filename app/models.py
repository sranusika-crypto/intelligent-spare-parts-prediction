
from sqlalchemy import Column, Integer, String
from app.database import Base


class SparePart(Base):
    __tablename__ = "spare_parts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    stock = Column(Integer, default=0)
    criticality = Column(String(20), default="Medium")
