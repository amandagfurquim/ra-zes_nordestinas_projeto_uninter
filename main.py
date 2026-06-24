import models
from fastapi import FastAPI, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from auth import get_password_hash, verify_password
import schemas, models, database  
from database import banco_engine, SessionLocal, get_db
from typing import List
from enum import Enum

models.Base.metadata.create_all(bind=banco_engine) 


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#criar usuário
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

#login
@app.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Credenciais inválidas")
    
    print("Usuário encontrado, verificando senha...")
    if not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=403, detail="Credenciais inválidas")
    
    return {"message": "Login realizado com sucesso!"}

#cadastro de produtos
@app.post("/produtos/", response_model=schemas.Produto, status_code=status.HTTP_201_CREATED)
def create_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    db_produto = models.Produto(**produto.model_dump())
    
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    
    return db_produto

#get usuários no swagger
@app.get("/users/", response_model=List[schemas.User]) # Ajuste conforme seu schema
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

#get produtos no swagger
@app.get("/produtos/", response_model=List[schemas.Produto])
def get_produtos(db: Session = Depends(database.get_db)):
    produtos = db.query(models.Produto).all()
    return produtos

#editar produtos
@app.put("/produtos/{produto_id}", response_model=schemas.Produto)
def update_produto(produto_id: int, produto_atualizado: schemas.ProdutoCreate, db: Session = Depends(database.get_db)):
    db_produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if not db_produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    for key, value in produto_atualizado.model_dump().items():
        setattr(db_produto, key, value)
        
    db.commit()
    db.refresh(db_produto)
    return db_produto

#deletar produtos
@app.delete("/produtos/{produto_id}")
def delete_produto(produto_id: int, db: Session = Depends(database.get_db)):
    db_produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if not db_produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    db.delete(db_produto)
    db.commit()
    return {"message": "Produto deletado com sucesso"}

#criar pedido com subtração de estoque
@app.post("/pedidos/", response_model=schemas.Pedido)
def create_pedido(pedido: schemas.PedidoCreate, db: Session = Depends(database.get_db)):
    produto = db.query(models.Produto).filter(models.Produto.id == pedido.produto_id).first()
    
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    if produto.estoque < pedido.quantidade:
        raise HTTPException(status_code=400, detail="Estoque insuficiente!")

    total_pedido = produto.preco * pedido.quantidade
    novo_pedido = models.Pedido(
            usuario_id=pedido.usuario_id,
            produto_id=pedido.produto_id,
            quantidade=pedido.quantidade,
            total=total_pedido,
            status="PENDENTE",
            forma_pagamento=pedido.forma_pagamento
        )
    
    produto.estoque -= pedido.quantidade
    
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)
    
    return novo_pedido

"""
#para atualizar o status do pedido 
@app.patch("/pedidos/{pedido_id}/status", response_model=schemas.Pedido)
def update_status_pedido(pedido_id: int, novo_status: str, db: Session = Depends(database.get_db)):
    pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()
    
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    pedido.status = novo_status
    
    db.commit()
    db.refresh(pedido)
    return pedido
"""

#Atualiza o status do pedido, mas com um menu suspenso, e não com um input. Veja schemas.py para ver o menu
@app.patch("/pedidos/{pedido_id}/status", response_model=schemas.Pedido)
def update_status_pedido(
    pedido_id: int, 
    novo_status: schemas.StatusPedido, 
    db: Session = Depends(database.get_db)
):
    pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()
    
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    pedido.status = novo_status
    
    db.commit()
    db.refresh(pedido)
    return pedido

