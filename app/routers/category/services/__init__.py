from .create import Create
from .create_sub import CreateSub
from .delete import Delete
from .delete_sub import DeleteSub
from .update import Update
from .get_all import GetAll


class CategoryService(Create, CreateSub, Delete, DeleteSub, Update, GetAll):
    pass


__all__ = ["CategoryService"]
