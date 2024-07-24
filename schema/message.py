from pydantic import BaseModel
from datetime import datetime

class MessageRender(BaseModel):
    id: int
    message: str
    image: str
    created_at: datetime