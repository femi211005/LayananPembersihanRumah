from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.pelanggan import Pelanggan
from schemas.pelanggan import PelangganCreate, PelangganResponse
from auth.jwt_handler import get_current_user

router = APIRouter(prefix="/pelanggan", tags=["Pelanggan"])

@router.post("/", response_model=PelangganResponse, status_code=status.HTTP_201_CREATED)
def create_pelanggan(request: PelangganCreate, db: Session = Depends(get_db), current_user: Pelanggan = Depends(get_current_user)):
    new_pelanggan = Pelanggan(**request.dict())
    db.add(new_pelanggan)
    db.commit()
    db.refresh(new_pelanggan)
    return new_pelanggan

@router.get("/", response_model=list[PelangganResponse])
def get_all_pelanggan(db: Session = Depends(get_db), current_user: Pelanggan = Depends(get_current_user)):
    return db.query(Pelanggan).all()

@router.get("/{id}", response_model=PelangganResponse)
def get_pelanggan_by_id(id: int, db: Session = Depends(get_db), current_user: Pelanggan = Depends(get_current_user)):
    pelanggan = db.query(Pelanggan).filter(Pelanggan.id == id).first()
    if not pelanggan:
        raise HTTPException(status_code=404, detail="Pelanggan tidak ditemukan")
    return pelanggan

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pelanggan(id: int, db: Session = Depends(get_db), current_user: Pelanggan = Depends(get_current_user)):
    pelanggan = db.query(Pelanggan).filter(Pelanggan.id == id).first()
    if not pelanggan:
        raise HTTPException(status_code=404, detail="Pelanggan tidak ditemukan")
    db.delete(pelanggan)
    db.commit()
    return None