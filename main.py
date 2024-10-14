from http import HTTPStatus as status
from fastapi import FastAPI, HTTPException

from app.routers import patients, doctors

app = FastAPI()

namespaces = (
    doctors,
    patients,
)

for namespace in namespaces:
    app.include_router(namespace.router)
