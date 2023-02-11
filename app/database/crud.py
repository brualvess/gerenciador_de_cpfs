from sqlalchemy.orm import Session
from .models import Cpf

async def create_cpf(cpf: str, db: Session):
    db.add(cpf)
    db.commit()

async def get_cpf(cpf: str, db: Session):
   return db.query(Cpf).filter(Cpf.cpf == cpf).first()

async def delete_cpf(cpf: str, db: Session):
    db.delete(cpf)
    db.commit()

async def get_all_cpf(db: Session):
    return db.query(Cpf.cpf, Cpf.createdAt).all()
    