from fastapi.responses import JSONResponse


def success_response(data, message: str = "Success", status_code: int = 200):
    return JSONResponse(
        status_code == status_code,
        content={
            "status": "success",
            "data": data,
            "message": message,
        },
    )
