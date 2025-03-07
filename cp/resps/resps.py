from pydantic import BaseModel
from starlette.responses import JSONResponse
from typing import Any
from sqlmodel import SQLModel


class Response:

    def __init__(self, data: SQLModel, status_code: int = 200):
        self.data = data 
        self.status_code = status_code

    def to_json(self):
        return JSONResponse(
            content=self.data.model_dump(mode="json"),
            status_code=self.status_code
        )