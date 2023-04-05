from pydantic import BaseModel, Field
from typing import Optional


class Items(BaseModel):
    _id: Optional[str] = Field(..., alias='_id')
    name: str
    description: str

    class Config:
        orm_mode = True
