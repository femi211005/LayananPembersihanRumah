from fastapi import FastAPI
from database import engine, Base
from routers import auth, pelanggan, pesanan # Pastikan pelanggan di-import

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Layanan Pembersihan Rumah API")

app.include_router(auth.router)
app.include_router(pelanggan.router) # Tambahkan ini
app.include_router(pesanan.router)