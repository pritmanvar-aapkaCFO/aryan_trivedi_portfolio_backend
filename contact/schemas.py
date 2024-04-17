from pydantic import BaseModel


class contact(BaseModel):
    name: str
    email: str
    message: str