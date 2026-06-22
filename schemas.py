from pydantic import BaseModel, EmailStr


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