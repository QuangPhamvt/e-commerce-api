from .get_list_users import GetList
from .create_demo_user import CreateDemoUser


class UserService(GetList, CreateDemoUser):
    pass


__all__ = ["UserService"]
