from cp.services.svc import ModelDeploymentService
from starlette.routing import Route
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.middleware import Middleware
from starlette.middleware.errors import ServerErrorMiddleware
from starlette.responses import JSONResponse
import uvicorn
from dynaconf import Dynaconf

class Main:

    def __init__(self, config):
        self.svc = ModelDeploymentService(config=config)

    def custom_exception_handler(request, exc):
        if isinstance(exc, HTTPException):
            return JSONResponse({"error": exc.detail}, status_code=exc.status_code)
        return JSONResponse({"error": "Unexpected Error"}, status_code=500)

    def __call__(self, *args, **kwargs):
        # Routes 
        routes = [
            Route("/health", self.svc.health, methods=["GET"]),
            Route("/modelDeployments", self.svc.create_or_update, methods=["POST"]),
            Route("/modelDeployments/{id}", self.svc.get, methods=["GET"]),
        ]

        return Starlette(routes=routes, debug=True, exception_handlers={Exception: self.custom_exception_handler})
    
if __name__ == "__main__":
    config = Dynaconf(settings_files=["settings.toml"])
    uvicorn.run(Main(config), host="0.0.0.0", port=3000, log_level="debug")


