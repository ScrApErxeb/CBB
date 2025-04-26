from pydantic import BaseModel
from typing import List

class FileUploadRequest(BaseModel):
    filepath: str
    user_id: str

class FileProcessingResponse(BaseModel):
    nb_chunks: int
    message: str
