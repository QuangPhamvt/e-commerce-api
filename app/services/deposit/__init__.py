from .create import Create
from .update import Update
from .get_by_id import GetById
from .get_list_deposit import GetList
from .delete import Delete


class DepositService(Create, Update, GetById, GetList, Delete):
    pass
