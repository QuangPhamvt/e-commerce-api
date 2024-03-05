from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str


class CreateRoleParam(RoleBase):
    pass


class Role(RoleBase):
    id: str
