from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth import get_password_hash, verify_password
import schemas, models, database  
from database import banco_engine, SessionLocal, get_db
from typing import List

models.Base.metadata.create_all(bind=banco_engine) 

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/usuarios/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Este e-mail já está cadastrado")
 
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password) # Chame a função aqui!
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Credenciais inválidas")
    
    print("Usuário encontrado, verificando senha...")
    if not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=403, detail="Credenciais inválidas")
    
    return {"message": "Login realizado com sucesso!"}
@app.post("/produtos/", response_model=schemas.Produto, status_code=status.HTTP_201_CREATED)
def create_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    db_produto = models.Produto(**produto.model_dump())
    
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    
    return db_produto

@app.get("/users/", response_model=List[schemas.User]) # Ajuste conforme seu schema
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.get("/produtos/", response_model=List[schemas.Produto])
def get_produtos(db: Session = Depends(database.get_db)):
    produtos = db.query(models.Produto).all()
    return produtos