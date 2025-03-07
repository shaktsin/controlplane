from starlette.requests import Request
from cp.models.db_handler import DBHandler
from cp.models.model_deployments import ModelDeployment, DeploymentJobs, Status
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from starlette.requests import Request
from cp.exceptions.exceptions import RuntimeException
from cp.resps.resps import Response


class ModelDeploymentService:

    def __init__(self):
        self.db_handler = DBHandler()
        self.db_handler.create_db_tables()

    async def health(self, request: Request):
        return JSONResponse(content="Hello, World!")

    async def create_or_update(self, req: Request) -> JSONResponse:
        data = await req.json()
        try:
            modelDep = ModelDeployment(**data)
            ModelDeployment.validate_model(modelDep.model)
        except Exception as e:
            print(e) # replace with logger 
            return RuntimeException(status_code=400, error=e).to_json()

        return self.db_handler.create_or_update_model_deployment(modelDep=modelDep).to_json()
    
    def get(self, id: int) -> ModelDeployment:
        with self.db_handler.get_session() as session:
            modelDep = session.get(ModelDeployment, id)
            if not modelDep:
                raise HTTPException(status_code=404, detail="ModelDeployment not found")
        return modelDep