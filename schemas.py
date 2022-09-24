from typing import Union
from pydantic import BaseModel


class TodoBase(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True

class TodoIn(TodoBase):
    pass

class TodoOut(TodoBase):
    id: Union[int, None] = None