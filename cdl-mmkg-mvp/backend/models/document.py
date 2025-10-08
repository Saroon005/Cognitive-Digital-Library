from pydantic import BaseModel
from typing import List


class DocumentResponse(BaseModel):
    text: str
    score: float
