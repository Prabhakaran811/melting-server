from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories.product_repository import ProductRepository
from app.schemas.product_schema import ProductCreate


class ProductService:

    @staticmethod
    def create_product(db: Session, product_data: ProductCreate):
        product_name = product_data.product_name.strip()

        if not product_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product name cannot be empty"
            )

        existing_product = ProductRepository.get_by_name(
            db, product_name
        )

        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product name already exists"
            )

        try:
            cleaned_data = ProductCreate(product_name=product_name)
            return ProductRepository.create(db, cleaned_data)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product name already exists"
            )

    @staticmethod
    def get_products(db: Session):
        return ProductRepository.get_all(db)

    @staticmethod
    def update_product(
        db: Session,
        product_id: int,
        product_data: ProductCreate
    ):
        product = ProductRepository.get_by_id(db, product_id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        product_name = product_data.product_name.strip()

        if not product_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product name cannot be empty"
            )

        existing_product = ProductRepository.get_by_name(
            db, product_name
        )

        if existing_product and existing_product.id != product_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product name already exists"
            )

        try:
            return ProductRepository.update(
                db, product, product_name
            )
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product name already exists"
            )

    @staticmethod
    def delete_product(db: Session, product_id: int):
        product = ProductRepository.get_by_id(db, product_id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        ProductRepository.delete(db, product)

        return {"message": "Product permanently deleted"}