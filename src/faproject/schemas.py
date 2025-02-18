from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    is_active: bool = False


class Token(BaseModel):
    access_token: str
    token_type: str


class ProviderResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class BlockBase(BaseModel):
    currency_name: str
    provider_name: str
    block_number: int
    block_created_at: Optional[datetime]
    stored_at: datetime

    class Config:
        from_attributes = True


class BlockResponse(BlockBase):
    id: int


class BlockList(BaseModel):
    total: int
    page: int
    page_size: int
    results: List[BlockResponse]
