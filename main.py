"""Starting point of app"""
from fastapi import FastAPI
from uvicorn import run

import configuration.constants as appConst
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

app.include_router(userAuth)


if __name__ == "__main__":
    run(app, host="127.0.0.1", port=8000)
