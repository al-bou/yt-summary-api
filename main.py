from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="YouTube Summary API")

app.include_router(router)
