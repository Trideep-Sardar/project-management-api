from fastapi import FastAPI
from starlette.exceptions import HTTPException
from app.core.exceptions import http_exception_handler, validation_exception_handler
from fastapi.exceptions import RequestValidationError
from app.api.v1 import router as v1_router

app = FastAPI(title="Project Management API")

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(v1_router)


@app.get("/")
def root():
    return {"message": "Project Management API is running"}
