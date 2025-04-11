from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.database import init_db
from routers import company_job, user_info, upload_router
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(company_job.router, prefix="/company")
app.include_router(user_info.router, prefix="/user")
app.include_router(upload_router.router, prefix="/upload")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (adjust if needed)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI Notes API is running"}
