from sqlmodel import Field, Session, SQLModel, create_engine, select, JSON
from cp.models.model_deployments import ModelDeployment, DeploymentJobs, Status
from typing import Dict, Any
from cp.jobs.jobs import WorkflowFactory, RedisJobs
from pydantic import BaseModel
from cp.exceptions.exceptions import RuntimeException
from cp.resps.resps import Response


class DBHandler:

    def __init__(self, config=None):
        self.sqlite_file = config["DEFAULT"]["DB"]
        self.sqlite_url = f"sqlite:///{self.sqlite_file}"
        connect_args = {"check_same_thread": False}
        self.engine = create_engine(self.sqlite_url, connect_args=connect_args)
        WorkflowFactory.register_workflow("redis", RedisJobs)
        self.config = config

    def create_db_tables(self):
        from sqlalchemy.orm import configure_mappers
        configure_mappers()
        SQLModel.metadata.create_all(self.engine)

    def get_session(self):
        with Session(self.engine) as session:
            return session
        

    def create_or_update_model_deployment(self, modelDep: ModelDeployment) -> Any:
        try:
            with self.get_session() as session:
                if not hasattr(modelDep, "id") or not modelDep.id:
                    session.add(modelDep)
                else:
                    modelDep1 = session.get(ModelDeployment, modelDep.id)
                    modelDep1.model = modelDep.model
                    modelDep1.resource = modelDep.resource
                    modelDep1.replicas = modelDep.replicas
                    modelDep1.status = Status.UPDATING
                    modelDep = modelDep1 
                
                
                session.commit()
                session.refresh(modelDep)
                #modelDep.url = f"{self.config["DEFAULT"]["DP_INGRESS_EP"]}/{modelDep.id}"

                job = DeploymentJobs(model_deployment_id=modelDep.id)
                session.add(job)
                session.commit()
                session.refresh(job)
                session.refresh(modelDep)

                task = WorkflowFactory.get_workflow("redis", config=self.config).submit(job.id, modelDep)
                job.workflow_job_id = task.id
                session.commit()
                session.refresh(modelDep)
            return Response(data=modelDep)
        except Exception as e:
            print(e) # replace with proper logger class
            return RuntimeException(error=Exception("Internal Server Error"), status_code=500)


