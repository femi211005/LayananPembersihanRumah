from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.pelanggan import Pelanggan
from schemas.pelanggan import PelangganCreate, PelangganResponse, Token, PelangganLogin
from auth.jwt_handler import create_access_token
from passlib.context import CryptContext

router = APIRouter(tags=["Auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", response_model=PelangganResponse, status_code=201)
def register(user: PelangganCreate, db: Session = Depends(get_db)):
    if db.query(Pelanggan).filter(Pelanggan.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email sudah terdaftar")
    
    new_user = Pelanggan(
        nama=user.nama, email=user.email, alamat=user.alamat,
        password=pwd_context.hash(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login(user: PelangganLogin, db: Session = Depends(get_db)):
    db_user = db.query(Pelanggan).filter(Pelanggan.nama == user.nama).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Nama atau password salah")
    
    token = create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}