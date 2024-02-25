TITLE: str = "E-Commerce API"
SUMMARY: str = "This is a simple API for E-Commerce"
VERSION: str = "0.0.1"
DOCS_URL: str = "/docs"
ROOT_PATH: str = "/api/v1"

USERS: str = "users"
ITEMS: str = "items"
CUSTOM: str = "custom"
ADMIN: str = "admin"

DB_PORT: int = 3306

DOCUMENTATIONS: dict = {
    "title": TITLE,
    "summary": SUMMARY,
    "version": VERSION,
    "docs_url": DOCS_URL,
    "root_path": ROOT_PATH,
    "openapi_tags": [
        {
            "name": USERS,
        },
        {
            "name": ITEMS,
        },
        {
            "name": CUSTOM,
        },
        {"name": ADMIN},
    ],
}
