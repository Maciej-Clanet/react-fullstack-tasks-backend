from pydantic import BaseModel
from typing import Literal, Optional


# "Literal" allows us to specify the exact values that are accepted
# | None = None makes this field optional
# Combined together means we don't have to provide a role, but if we do it will have to be one of these values
class AddPerson(BaseModel):
    name: str
    age: int
    role: Optional[Literal["admin", "manager", "supporter", "goober"]] = "goober"


class AddPersonResponse(BaseModel):
    message: str
    id: str


class UpdatePerson(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    role: Optional[Literal["admin", "manager", "staff", "customer", "goober"]] = None
