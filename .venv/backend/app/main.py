from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.router import router

app = FastAPI()

origins = [
        "http://localhost:3000",  # React URL
        # other origins if needed
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
   )

app.include_router( router )

@app.get("/")
async def root():
    return {"message": "Hello World"}
