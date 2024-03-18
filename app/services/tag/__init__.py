from .create import Create
from .delete import Delete
from .get_all import GetAll


class TagService(Create, Delete, GetAll):
    pass


__all__ = ["TagService"]
