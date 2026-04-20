from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.pesanan import Pesanan
from schemas.pesanan import PesananCreate, PesananResponse
from auth.jwt_handler import get_current_user

router = APIRouter(prefix="/pesanan", tags=["Pesanan"])

@router.post("/", response_model=PesananResponse, status_code=status.HTTP_201_CREATED)
def create_pesanan(request: PesananCreate, db: Session = Depends(get_db), current_user: Pesanan = Depends(get_current_user)):
    new_pesanan = Pesanan(**request.dict())
    db.add(new_pesanan)
    db.commit()
    db.refresh(new_pesanan)
    return new_pesanan

@router.get("/", response_model=list[PesananResponse])
def list_pesanan(db: Session = Depends(get_db), current_user: Pesanan = Depends(get_current_user)):
    return db.query(Pesanan).all()

@router.get("/{id}", response_model=PesananResponse)
def get_pesanan_by_id(id: int, db: Session = Depends(get_db), current_user: Pesanan = Depends(get_current_user)):
    pesanan = db.query(Pesanan).filter(Pesanan.id == id).first()
    if not pesanan:
        raise HTTPException(status_code=404, detail="Pesanan tidak ditemukan")
    return pesanan

@router.put("/{id}", response_model=PesananResponse)
def update_pesanan(id: int, request: PesananCreate, db: Session = Depends(get_db), current_user: Pesanan = Depends(get_current_user)):
    pesanan_query = db.query(Pesanan).filter(Pesanan.id == id)
    if not pesanan_query.first():
        raise HTTPException(status_code=404, detail="Pesanan tidak ditemukan")
    pesanan_query.update(request.dict())
    db.commit()
    return pesanan_query.first()