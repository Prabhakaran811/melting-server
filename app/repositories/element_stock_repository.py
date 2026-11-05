from sqlalchemy.orm import Session, joinedload

from app.models.element_stock import ElementStock
from app.models.element import Element
from app.models.supplier import Supplier


class ElementStockRepository:

    @staticmethod
    def create(db: Session, data: dict):
        try:
            stock = ElementStock(**data)

            db.add(stock)
            db.commit()
            db.refresh(stock)

            return ElementStockRepository.get_by_id(
                db, stock.id
            )

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_all(db: Session):
        return (
            db.query(ElementStock)
            .options(
                joinedload(ElementStock.element),
                joinedload(ElementStock.supplier)
            )
            .order_by(ElementStock.id.desc())
            .all()
        )

    @staticmethod
    def get_by_id(db: Session, stock_id: int):
        return (
            db.query(ElementStock)
            .options(
                joinedload(ElementStock.element),
                joinedload(ElementStock.supplier)
            )
            .filter(ElementStock.id == stock_id)
            .first()
        )

    @staticmethod
    def get_element_by_id(db: Session, element_id: int):
        return db.query(Element).filter(
            Element.id == element_id
        ).first()

    @staticmethod
    def get_supplier_by_id(db: Session, supplier_id: int):
        return db.query(Supplier).filter(
            Supplier.id == supplier_id
        ).first()

    @staticmethod
    def update(db: Session, stock, data: dict):
        try:
            for key, value in data.items():
                setattr(stock, key, value)

            db.commit()
            db.refresh(stock)

            return ElementStockRepository.get_by_id(
                db, stock.id
            )

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def delete(db: Session, stock):
        try:
            db.delete(stock)
            db.commit()

        except Exception:
            db.rollback()
            raise