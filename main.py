from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import patients, doctors, auth, users


app = FastAPI()

origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


namespaces = (
    auth,
    doctors,
    patients,
    users
)

for namespace in namespaces:
    app.include_router(namespace.router)
