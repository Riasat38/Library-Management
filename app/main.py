from fastapi import FastAPI
from app.routes.books import router as books_router
from app.database import engine, Base
from app.models import db_models 

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API")

# Include the books router
app.include_router(books_router, tags=["Books"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Library Management API"}
