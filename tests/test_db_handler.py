import pytest 
from cp.models.db_handler import DBHandler
from cp.models.model_deployments import ModelDeployment, Model, ModelType, Resource
import logging 


def mock_db_handler():
    """Mock DB Handler"""
    config = {
        "DEFAULT": {
            "DB": "/tmp/md.db"
        }
    }
    return DBHandler(config)


def test_create_or_update_model_deployment():
    model_dep = ModelDeployment()
    model_dep.model = Model(type=ModelType.SINGLE, version="1.0", bucket="s3://dummy", prefix="/abc")
    model_dep.request_res = Resource(cpu="500m", memory="1Gi", gpu=1)
    model_dep.limit_res = Resource(cpu="500m", memory="1Gi", gpu=1)
    
    returned = mock_db_handler().create_or_update_model_deployment(model_dep)
    assert returned is not None 


