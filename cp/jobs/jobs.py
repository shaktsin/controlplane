from abc import ABC, abstractmethod
from celery import Celery
from cp.models.model_deployments import ModelDeployment
from typing import Any

class Job(ABC):
    @abstractmethod
    def submit(self, *arg, **kwargs) -> Any:
        pass 

    @abstractmethod
    def status(self, job_id: str) -> Any:
        pass 


class RedisJobs(Job):

    def __init__(self, config=None):
        super().__init__()
        self.app = Celery(
            "tasks",
            broker=config["DEFAULT"]["BROKER"]
        )

    def submit(self, job_id: int, modelDep: ModelDeployment):
        print("before", job_id, modelDep)
        return self.app.send_task(
            "main.process_job",
            args = [job_id, modelDep.model_dump()]
        )
    
    def status(self, job_id: str) -> Any:
        return self.app.AsyncResult(job_id) 
    

class WorkflowFactory:
    _workflows = {}

    @classmethod
    def register_workflow(cls, type, workflow_cls):
        cls._workflows[type] = workflow_cls

    @classmethod
    def get_workflow(cls, workflow_cls, config):
        if workflow_cls not in cls._workflows:
            raise ValueError(f"Unknown workflow type: {workflow_cls}")
        return cls._workflows[workflow_cls](config)
 
