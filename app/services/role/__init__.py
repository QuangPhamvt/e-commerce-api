from .create import Create
from .delete import Delete
from .update import Update
from .get_all import GetAll


class RoleService(Create, Delete, Update, GetAll):
    pass


__all__ = ["RoleService"]
