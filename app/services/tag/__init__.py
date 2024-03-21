from .create import Create
from .delete import Delete
from .get_all import GetAll
from .add_product_tag import AddProductTag


class TagService(Create, Delete, GetAll, AddProductTag):
    pass


__all__ = ["TagService"]
