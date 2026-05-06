from fastapi import FastAPI
from app.routes.users import router as users_router

app = FastAPI(title="User Data Service", version="1.0.0")
app.include_router(users_router)
