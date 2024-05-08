from .sign_up import SignUp
from .verify import Verify
from .sign_in import SignIn
from .logout import Logout
from .refresh import Refresh
from .get_me import GetMe
from .forgot import Forgot
from .reset_password import ResetPassword
from .oauth2 import GoogleAuth, FacebookAuth

class AuthService(
    SignUp, Verify, SignIn, Logout, Refresh, GetMe, Forgot, ResetPassword, GoogleAuth, FacebookAuth
):
    pass


__all__ = ["AuthService"]
