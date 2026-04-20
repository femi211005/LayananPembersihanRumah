# models/pesanan.py
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base # Pastikan Base di-import dari database.py

class Pesanan(Base):
    __tablename__ = "pesanan"

    id = Column(Integer, primary_key=True, index=True)
    item_type = Column(String, nullable=False) 
    item_name = Column(String, nullable=False) 
    service_type = Column(String, nullable=False) 
    booking_date = Column(Date, nullable=False)
    status = Column(String, default="pending")
    
    pelanggan_id = Column(Integer, ForeignKey("pelanggan.id"), nullable=False)
    
    # Relasi balik ke Pelanggan
    pemilik = relationship("Pelanggan", back_populates="pesanan")