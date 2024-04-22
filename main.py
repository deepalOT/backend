from fastapi import FastAPI, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from fastapi.middleware.cors import CORSMiddleware
from src.app import router as app_router

app = FastAPI()
origins = ["http://localhost:3000","https://dshboard-three.vercel.app", "0.0.0.0"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def index():
    return {"status": "ok"}


app.include_router(app_router.router)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)