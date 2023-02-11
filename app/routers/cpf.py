from fastapi import APIRouter, HTTPException, Body
from ..internal.cpf_validation import validate
from fastapi.responses import JSONResponse
from ..database import crud, database, models
from sqlalchemy.orm import Session
from fastapi import Depends
from datetime import datetime

router = APIRouter()


def get_db():
    db = database.Session()
    try:
        yield db
    finally:
        db.close()


@router.post("/cpf")
async def create(cpf: str = Body(embed=True),  db: Session = Depends(get_db)):
    verify_cpf = validate(cpf)
    if (not verify_cpf):
        return JSONResponse(
            status_code=400,
            content={"type": "InvalidCpfException",
                     "message": "CPF is not valid."}
        )
    get_cpf = await crud.get_cpf(cpf, db)
    if (get_cpf):
        return JSONResponse(
            status_code=409,
            content={"type": "ExistsCpfException",
                     "message": "Cpf already exists."})

    date = datetime.now().isoformat()
    date_format = datetime.fromisoformat(date)
    data = models.Cpf()
    data.cpf = cpf
    data.createdAt = date_format
    await crud.create_cpf(data, db)
    return JSONResponse(
        status_code=201,
        content={"message": "Created."}
    )


@router.get("/cpf/{cpf}")
async def get_by_cpf(cpf, db: Session = Depends(get_db)):
    verify_cpf = validate(cpf)
    if (not verify_cpf):
        return JSONResponse(
            status_code=400,
            content={"type": "InvalidCpfException",
                     "message": "CPF is not valid."}
        )

    get_cpf = await crud.get_cpf(cpf, db)
    if (not get_cpf):
        return JSONResponse(
            status_code=404,
            content={"type": "NotFoundCpfException",
                     "message": "Cpf not found."})

    return JSONResponse(
        status_code=200,
        content={"cpf": get_cpf.cpf,
                 "createdAt": get_cpf.createdAt.isoformat()}
    )


@router.delete("/cpf/{cpf}")
async def delete(cpf, db: Session = Depends(get_db)):
    verify_cpf = validate(cpf)
    if (not verify_cpf):
        return JSONResponse(
            status_code=400,
            content={"type": "InvalidCpfException",
                     "message": "CPF is not valid."}
        )
    get_cpf = await crud.get_cpf(cpf, db)
    if (not get_cpf):
        return JSONResponse(
            status_code=404,
            content={"type": "NotFoundCpfException",
                     "message": "Cpf not found."})
    await crud.delete_cpf(get_cpf,db)
    return JSONResponse(
            status_code=200,
            content={"message":"Deleted."})

@router.get("/cpf")
async def get_all(db: Session = Depends(get_db)):
    result =  await crud.get_all_cpf(db)
    response = [{"cpf": data[0], "createdAt": data[1]}for data in result]
    return response