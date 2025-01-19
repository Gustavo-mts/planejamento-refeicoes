from fastapi import FastAPI
from app.database import init_db
from app.routers import ingrediente, receitas, planejamento

app = FastAPI(title="Gerenciador de Receitas")

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(ingrediente.router)
app.include_router(receitas.router)
app.include_router(planejamento.router)
