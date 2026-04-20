from pydantic import BaseModel
from datetime import date

class PesananBase(BaseModel):
    item_type: str
    item_name: str
    service_type: str
    booking_date: date
    pelanggan_id: int

class PesananCreate(PesananBase):
    pass

class PesananResponse(PesananBase):
    id: int
    class Config:
        from_attributes = True