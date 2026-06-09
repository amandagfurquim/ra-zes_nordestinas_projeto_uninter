from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, models
from database import engine, SessionLocal


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="PROJ_RAIZES_NORDESTINAS")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Bem-vinda ao sistema PROJ_RAIZES_NORDESTINAS!"}

@app.post("/usuarios/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Este e-mail já está cadastrado")
    
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=user.password  # Vamos criptografar logo logo!
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user