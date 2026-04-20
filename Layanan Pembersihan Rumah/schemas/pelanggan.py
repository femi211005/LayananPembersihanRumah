from pydantic import BaseModel, EmailStr

class PelangganBase(BaseModel):
    nama: str
    email: EmailStr
    alamat: str

class PelangganCreate(PelangganBase):
    password: str

class PelangganLogin(BaseModel):
    nama: str
    password: str

class PelangganResponse(PelangganBase):
    id: int
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str