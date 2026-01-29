from pydantic import BaseModel
from typing import Optional, List

class RepositoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_private: bool = False

class RepositoryCreate(RepositoryBase):
    pass

class Repository(RepositoryBase):
    id: str
    owner: str
    files: List[str] = []

    class Config:
        from_attributes = True
