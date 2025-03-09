import pytest 
from cp.models.db_handler import DBHandler
from cp.models.model_deployments import ModelDeployment, Model, ModelType, Resource
import logging 
from starlette.requests import Request
from unittest.mock import MagicMock, AsyncMock
from cp.services.svc import ModelDeploymentService

@pytest.fixture
def mock_request():
    """Creates a fake Starlette request with a mock session."""
    request = MagicMock(spec=Request)
    request.json = AsyncMock({
                "type": "cpu",
                "model": {
                    "version": "v1",
                    "type": "single",
                    "bucket": "s3://demmodels/",
                    "prefix": "models"
                },
                "replicas": 1,
                "request_res": {
                    "cpu": "500m",
                    "memory": "512Mi"
                },
                "limit_res": {
                    "cpu": "1",
                    "memory": "1Gi"
                }
            })  
    
    return request

def mock_svc():
    """Mock DB Handler"""
    config = {
        "DEFAULT": {
            "DB": "/tmp/md.db"
        }
    }
    return ModelDeploymentService(config)

@pytest.mark.asyncio
async def test_create(mock_request):
    mock_svc = mock_svc()

    req_data = await mock_svc.create_or_update(mock_request)
    assert req_data is not None
    mock_request.json.assert_called_once()  # Ensure request.json() was called

@pytest.mark.asyncio
async def test_get(mock_request):
    mock_svc = mock_svc()

    req_data = await mock_svc.get(mock_request)
    assert req_data is not None
    mock_request.json.assert_called_once()  # Ensure request.json() was called

