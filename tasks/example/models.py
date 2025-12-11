from pydantic import BaseModel
from typing import Literal


# "Literal" allows us to specify the exact values that are accepted
# | None = None makes this field optional
# Combined together means we don't have to provide a role, but if we do it will have to be one of these values
class AddPerson(BaseModel):
    name: str
    age: int
    role: Literal["admin", "manager", "supporter", "goober"] | None = None


class AddPersonResponse(BaseModel):
    message: str
    id: str


class UpdatePerson(BaseModel):
    name: str | None = None
    age: int | None = None
    role: Literal["admin", "manager", "staff", "customer", "goober"] | None = None
