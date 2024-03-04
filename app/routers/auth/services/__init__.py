from .sign_up import SignUp
from .verify import Verify


class AuthService(SignUp, Verify):
    pass


__all__ = ["AuthService"]
