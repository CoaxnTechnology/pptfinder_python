from pydantic import BaseModel
from typing import Any, List, Optional


# -------------------------
# Request Schemas
# -------------------------

class CheckKeywordRequest(BaseModel):
    keyword: str


class SaveDataItem(BaseModel):
    title: Optional[str] = None
    link: Optional[str] = None
    displayLink: Optional[str] = None
    mime: Optional[str] = None
    fileFormat: Optional[str] = None
    snippet: Optional[str] = None


class SaveDataRequest(BaseModel):
    keyword: str
    results: List[SaveDataItem]


# -------------------------
# Response Schemas
# -------------------------

class CheckKeywordResponse(BaseModel):
    exists: bool
    object: Optional[Any] = None

    model_config = {
        "from_attributes": True
    }


class SaveDataResponse(BaseModel):
    message: str
    saved: bool


# -------------------------
# Category API Response
# -------------------------

class CategoryItem(BaseModel):
    id: int
    category: str

class CategoryResponse(BaseModel):
    status: str
    data: List[CategoryItem]
