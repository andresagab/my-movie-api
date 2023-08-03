from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

# define class
class ErrorHandler(BaseHTTPMiddleware):

    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)

    # define async method to manage errors, when a error is produced in our app
    async def dispatch(self, request: Request, call_next) -> Response | JSONResponse:
        # try execute request
        try:
            return await call_next(request)
        # except return json response with error (500)
        except Exception as e:
            return JSONResponse(status_code = 500, content = {'error': str(e)})
