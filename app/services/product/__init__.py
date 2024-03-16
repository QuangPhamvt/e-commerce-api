from .get_products import GetProducts
from .create_product import CreateProduct
from .update_product_by_id import UpdateProductById
from .delete_product_by_id import DeleteProductById


class ProductService(CreateProduct, GetProducts, DeleteProductById, UpdateProductById):
    pass
