from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router

app = FastAPI(title="YouTube Summary API")

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔐 Remplace "*" par ton domaine de frontend si tu veux restreindre
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
