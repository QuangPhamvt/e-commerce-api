from app.configs.constants import CLOUDFRONT_URL


def get_image_from_url(path: str) -> str:
    return f"{CLOUDFRONT_URL}/{path}"
