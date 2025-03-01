from fastapi import FastAPI
from routers import company_job
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(company_job.router, prefix="/api")

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