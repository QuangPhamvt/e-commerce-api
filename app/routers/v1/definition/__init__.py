from fastapi import APIRouter
from .category import router as category_router
from .product import router as product_router
from .series import router as series_router
from .tag import router as tag_router

router = APIRouter()


router.include_router(category_router)
router.include_router(product_router)
router.include_router(series_router)
router.include_router(tag_router)
