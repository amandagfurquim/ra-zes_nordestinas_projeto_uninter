API - Raízes Nordestinas - Trabalho Backend Uninter 
API Rest desenvolvida com o objetivo de automatizar os pedidos em um restaurante 
Tecnilogias Utilizadas: 
* Linguagem Python 3.10
* Framework: FastAPI
* Banco de dados: SQLAlquemy com SQLite para vizualisar o banco
* Ferramentas de IA: Google Gemini 
* Validação de dados: Pydantic
* Segurança: Bcrypt para criar o hash
* Documentação: Swagger UI/OpenAPI

  Estrutura do Projeto
* `main.py`: Ponto de entrada da aplicação, contendo as rotas (endpoints) e regras de negócio.
* `models.py`: Modelagem do banco de dados relacional (Tabelas: Users, Produtos, Pedidos).
* `schemas.py`: Contratos de entrada/saída de dados via Pydantic e classes Enum.
* `database.py`: Configuração da conexão com o banco de dados SQLite.

Como executar o programa localmente:
1. Clone o repositório ou extraia os arquivos
2. Instale as dependencias necessárias: pip install fastapi[all] sqlalchemy bcrypt passlib
3. Inicie o servidor local: uvicorn main:app --reload
4. Para acessar a documentação: http://127.0.0.1:8000/docs

Principais funcionalidades:
POST /usuarios/: Cria um novo usuário com validação de e-mail único e criptografia de senha.
POST /produtos/: Cadastra produtos com preço e quantidade em estoque.
POST /pedidos/: Realiza uma venda. O sistema valida se o usuário e o produto existem, verifica se há estoque suficiente, calcula o valor total e debita o produto do estoque automaticamente.

Desenvolvido por Amanda Furquim 
