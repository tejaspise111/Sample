from fastapi import FastAPI, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from database import get_db, Base, engine
from models import User
from schemas import UserCreate, UserLogin
from auth import hash_password, verify_password, create_access_token


from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Mount static files (for frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create database tables
Base.metadata.create_all(bind=engine)

@app.post("/signup/")
def signup(username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(password)
    new_user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

@app.post("/login/")
def login( email: str = Form(...),
    password: str = Form(...), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user or not verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    token = create_access_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}


