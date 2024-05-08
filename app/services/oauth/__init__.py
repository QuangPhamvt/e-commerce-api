
from app.services.oauth.oauth2 import FacebookAuth, GoogleAuth


class OauthService(
    GoogleAuth, FacebookAuth
):
    pass


__all__ = ["AuthService"]
