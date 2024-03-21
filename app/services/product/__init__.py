from .get_products import GetProducts
from .create_product import CreateProduct
from .update_product_by_id import UpdateProductById
from .delete_product_by_id import DeleteProductById
from .get_products_by_tag import GetProductsByTag


class ProductService(
    CreateProduct, GetProducts, DeleteProductById, UpdateProductById, GetProductsByTag
):
    pass
