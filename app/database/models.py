from .database import Base
from sqlalchemy import Column,Integer, DateTime, VARCHAR

class Cpf(Base):
    __tablename__ = 'cpfs'

    id = Column(Integer, primary_key=True)
    cpf = Column(VARCHAR(11), unique=True, nullable=False)
    createdAt = Column(DateTime)
