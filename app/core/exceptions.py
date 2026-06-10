from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.logger import setup_logger

logger = setup_logger(__name__)


class AppException(HTTPException):
    def __init__(self, status_code: int, message: str):
        super().__init__(status_code=status_code, detail=message)


async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"{request.method} {request.url} - {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "code": exc.status_code,
            "message": exc.detail,
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation Error : {request.method} {request.url}")
    errors = []
    for error in exc.errors():
        errors.append(
            {"field": "->".join(str(e) for e in error["loc"]), "message": error["msg"]}
        )
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "code": 422,
            "message": "Validation failed",
            "errors": errors,
        },
    )
