"""Starting point of app"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

import configuration.constants as appConst
from configuration import configure
from db.db_setup import Base, engine
from features.authentication.routes import userAuth

Base.metadata.create_all(bind=engine)
# Base.metadata.create_all(bind=async_engine)

app = FastAPI(
    title=appConst.PROJECT_TITLE,
    description=appConst.PROJECT_DESCRIPTION,
    version=appConst.PROJECT_VERSION,
    contact=appConst.contactInfo,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=configure.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(userAuth)


if __name__ == "__main__":
    run(app, host="127.0.0.1", port=8000)
