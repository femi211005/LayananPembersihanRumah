from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Pelanggan(Base):
    __tablename__ = "pelanggan"
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    alamat = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False)
    
    # Relasi: Satu pelanggan memiliki banyak pesanan [cite: 32]
    pesanan = relationship("Pesanan", back_populates="pemilik", cascade="all, delete-orphan")