from fastapi import APIRouter,Depends, Query, HTTPException
from database.connecter import create_session
from prescription.tables import Prescription
from sqlmodel import select

prescription_router = APIRouter(
    tags=["prescription"],
)

@prescription_router.get("/all")
def get_all_prescriptions(
    limit: int = Query(10, ge=1, description="Number of items to return"),
    offset: int = Query(0, description="Number of items to skip"),
    session = Depends(create_session),
):
    total = session.query(Prescription).count()
    prescriptions = session.exec(select(Prescription).offset(offset).limit(limit)).all()
    
    return {
        "data": prescriptions,
        "total": total,
        "limit": limit,
        "offset": offset,
    }

@prescription_router.get("/get/{pres_id}")
def get_prescription(pres_id, session = Depends(create_session)):
    prescription = session.exec(select(Prescription).where(Prescription.id == pres_id)).first()
    if not prescription:
        return {"error" : "record not found"}
    return prescription

@prescription_router.post("/add")
def add_prescription(prescription : Prescription, session = Depends(create_session)):
    session.add(prescription)
    session.commit()
    session.refresh(prescription)
    return prescription   

@prescription_router.delete("/delete/{pres_id}")
def delete_prescription(pres_id: int, session = Depends(create_session)):

    prescription = session.get(Prescription, pres_id)
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")

    session.delete(prescription)
    session.commit()
    return {"ok": True}

@prescription_router.patch("/edit/{pres_id}")
def update_prescription(pres_id: int, prescription: Prescription, session=Depends(create_session)):
 
    db_prescription = session.get(Prescription, pres_id)
    if not db_prscription:
            raise HTTPException(status_code=404, detail="Prescription not found")
    prescripttion_data = prescription.dict(exclude_unset=True)
    for key, value in prscription_data.items():
        setattr(db_prescription, key, value)
        session.add(db_prescription)
        session.commit()
        session.refresh(db_prescription)
        return db_prescription
