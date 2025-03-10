from pydantic import BaseModel
from typing import List
import datetime as dt

class Mail(BaseModel):
    subject: str
    sender: str
    reciever: list[str]
    time: str
    content: list[str]
    response: str
    category: str 
    is_important: bool
    tags: list[str]