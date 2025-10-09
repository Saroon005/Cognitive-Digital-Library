from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


class DocumentBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    content: str = Field(..., min_length=1)
    authors: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    file_path: Optional[str] = None
    metadata: Optional[dict] = Field(default_factory=dict)


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    content: Optional[str] = None
    authors: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    metadata: Optional[dict] = None


class DocumentInDB(DocumentBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    upload_date: datetime = Field(default_factory=datetime.utcnow)
    content_embedding: Optional[List[float]] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}


class DocumentResponse(DocumentBase):
    id: str = Field(alias="_id")
    upload_date: Optional[datetime] = None
    
    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat() if v else None}


class DocumentSearchResponse(BaseModel):
    id: str = Field(alias="_id")
    title: str
    content: str
    authors: List[str]
    tags: List[str]
    score: float
    upload_date: Optional[datetime] = None
    
    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat() if v else None}
