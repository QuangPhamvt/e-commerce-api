from .create import Create
from .update import Update
from .delete import Delete
from .get_all import GetAll


class SeriesService(Create, Update, Delete, GetAll):
    pass


__all__ = ["SeriesService"]
