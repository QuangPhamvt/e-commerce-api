from app.services.user.get_by_id import GetById
from .get_list_users import GetList
from .create_demo_user import CreateDemoUser
from .create import Create
from .update import Update
from .delete import Delete
    
class UserService(Create, Update, Delete, GetById, GetList, CreateDemoUser):
    pass


__all__ = ["UserService"]
