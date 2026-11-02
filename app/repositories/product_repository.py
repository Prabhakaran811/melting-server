from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product_schema import ProductCreate


class ProductRepository:

    @staticmethod
    def create(db: Session, product_data: ProductCreate):
        product = Product(**product_data.model_dump())

        try:
            db.add(product)
            db.commit()
            db.refresh(product)
            return product
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_all(db: Session):
        return (
            db.query(Product)
            .order_by(Product.id.desc())
            .all()
        )

    @staticmethod
    def get_by_id(db: Session, product_id: int):
        return (
            db.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

    @staticmethod
    def get_by_name(db: Session, product_name: str):
        return (
            db.query(Product)
            .filter(Product.product_name == product_name)
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        product: Product,
        product_name: str
    ):
        try:
            product.product_name = product_name

            db.commit()
            db.refresh(product)

            return product
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def delete(db: Session, product: Product):
        try:
            db.delete(product)
            db.commit()
            return True
        except Exception:
            db.rollback()
            raise