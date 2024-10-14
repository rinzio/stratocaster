from fastapi import FastAPI
from app.routers import patients, doctors

app = FastAPI()

namespaces = (
    doctors,
    patients,
)

for namespace in namespaces:
    app.include_router(namespace.router)
