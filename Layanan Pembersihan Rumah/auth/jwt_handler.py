from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from models.pelanggan import Pelanggan

SECRET_KEY = "geby_secret_key_unhas"
ALGORITHM = "HS256"
security = HTTPBearer() # Untuk tombol Authorize di Swagger [cite: 28]

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(db: Session = Depends(get_db), auth: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(auth.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token tidak valid")
    except JWTError:
        raise HTTPException(status_code=401, detail="Kredensial tidak valid")
    
    user = db.query(Pelanggan).filter(Pelanggan.id == int(user_id)).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User tidak ditemukan")
    return user