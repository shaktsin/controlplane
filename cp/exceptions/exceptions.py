from starlette.responses import JSONResponse

class RuntimeException:
    
    def __init__(self, status_code: int, error: Exception):
        self.status_code = status_code 
        self.error = str(error)

    def to_json(self):
        return JSONResponse(
            content=self.__dict__,
            status_code=self.status_code
        )