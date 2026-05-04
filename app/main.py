from fastapi import FastAPI
from app.routes.books import router as books_router
from app.database import engine, Base, create_tables
from app.models import db_models 
from app.routes import members

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API")

# Include the books router
app.include_router(books_router, tags=["Books"])
app.include_router(members.router)

@app.on_event("startup")
def on_startup():
    create_tables()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Library Management API"}
