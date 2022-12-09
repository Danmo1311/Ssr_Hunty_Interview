from typing import List

from fastapi import FastAPI
from service_layer import handlers
from domain import commands, events

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}


### RETO
@app.get("/recomendacion/{user_id}", response_model=List[events.Vacante])
def recomendar_vacante(user_id: str):
    return handlers.recomendacion_vacantes(user_id=user_id)  # user_skills=skills)


### Vacantes
@app.get("/vacantes", response_model=List[events.Vacante])
def obtener_vacantes():
    return handlers.get_vacantes()


@app.post("/vacantes")
def añadir_vacantes(vacantes: List[commands.Vacante], company_name: str):
    return handlers.create_vacantes(company_name=company_name, vacantes=vacantes)


@app.get("/vacantes/{vacante_id}", response_model=events.Vacante)
def vancantes_por_id(vacante_id: str):
    return handlers.get_vacante_by_id(vacante_id=vacante_id)


@app.put("/vacantes/{vacante_id}", response_model=events.Vacante)
def actualizar_vancante(vacante: commands.Vacante, vacante_id: str):
    return handlers.actualizar_vacante(vacante=vacante, vacante_id=vacante_id)


@app.delete("/vacantes/{vacante_id}")
def eliminar_vancante(vacante_id: str):
    return handlers.eliminar_vacante(vacante_id=vacante_id)


### Usuarios
@app.get("/usuarios", response_model=List[events.Usuario])
def obtener_usuarios():
    return handlers.get_usuarios()


@app.get("/usuario/{user_id}", response_model=events.Usuario)
def usuario_por_id(user_id: str):
    return handlers.get_usuario_by_id(user_id=user_id)


@app.post("/usuarios")
def crear_usuario(usuario: List[commands.Usuario]):
    return handlers.create_usuarios(usuarios=usuario)


@app.put("/usuario/{user_id}", response_model=events.Usuario)
def actualizar_usuario(usuario: commands.Usuario, user_id: str):
    return handlers.actualizar_usuario(usuario=usuario, user_id=user_id)


@app.delete("/usuario/{user_id}")
def eliminar_usuario(user_id: str):
    return handlers.eliminar_usuario(user_id=user_id)


### Empresas
@app.get("/empresas", response_model=List[events.Empresa])
def obtener_empresas():
    return handlers.get_empresas()


@app.get("/empresa/{empresa_id}", response_model=events.Empresa)
def empresa_por_id(empresa_id: str):
    return handlers.get_empresas_by_id(empresa_id=empresa_id)


@app.post("/empresas")
def crear_empresas(empresas: List[commands.Empresa]):
    return handlers.create_empresas(empresas=empresas)


@app.put("/empresa/{empresa_id}", response_model=events.Empresa)
def actualizar_empresa(empresa: commands.Empresa, empresa_id: str):
    return handlers.actualizar_empresa(empresa=empresa, empresa_id=empresa_id)


@app.delete("/empresa/{empresa_id}")
def eliminar_empresa(empresa_id: str):
    return handlers.eliminar_empresa(empresa_id=empresa_id)
