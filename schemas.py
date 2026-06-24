from pydantic import BaseModel, EmailStr
from enum import Enum

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ProdutoBase(BaseModel):
    nome: str
    descricao: str | None = None
    preco: float
    estoque: int

class ProdutoCreate(ProdutoBase):
    pass

class Produto(ProdutoBase):
    id: int

    class Config:
        from_attributes = True

class User(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

class PedidoCreate(BaseModel):
    usuario_id: int
    produto_id: int
    quantidade: int

class Pedido(PedidoCreate):
    id: int
    total: float
    status: str

    class Config:
        from_attributes = True

class StatusPedido(str, Enum):
    PENDENTE = "PENDENTE"
    EM_PREPARO = "EM PREPARO"
    CONCLUIDO = "CONCLUIDO"
    CANCELADO = "CANCELADO"

class PedidoCreate(BaseModel):
    usuario_id: int
    produto_id: int
    quantidade: int

class Pedido(PedidoCreate):
    id: int
    total: float
    status: StatusPedido 

    class Config:
        from_attributes = True

class PedidoCreate(BaseModel):
    usuario_id: int
    produto_id: int
    quantidade: int
    forma_pagamento: str

#lista do status de pedido para ser selecionado, e não escrito
class StatusPedido(str, Enum):
    PENDENTE = "PENDENTE"
    EM_PREPARO = "EM PREPARO"
    CONCLUIDO = "CONCLUIDO"
    CANCELADO = "CANCELADO"

#lista de formas de pagamento para ser selecionado
class FormaPagamento(str, Enum):
    PIX = "PIX"
    CARTAO_CREDITO = "CARTAO CREDITO"
    CARTAO_DEBITO = "CARTAO DEBITO"
    DINHEIRO = "DINHEIRO"

class PedidoCreate(BaseModel):
    usuario_id: int
    produto_id: int
    quantidade: int
    forma_pagamento: FormaPagamento

class Pedido(PedidoCreate):
    id: int
    total: float
    status: StatusPedido

    class Config:
        from_attributes = True