from .sign_up import SignUp
from .verify import Verify
from .sign_in import SignIn
from .logout import Logout
from .refresh import Refresh
from .get_me import GetMe


class AuthService(SignUp, Verify, SignIn, Logout, Refresh, GetMe):
    pass


__all__ = ["AuthService"]
