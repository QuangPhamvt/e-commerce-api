from app.configs.constants import CLOUNDFRONT_URL


def get_image_from_url(path: str) -> str:
    return f"{CLOUNDFRONT_URL}/{path}"
