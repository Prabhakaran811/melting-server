from sqlalchemy.orm import Session, joinedload

from app.models.wire_stock import WireStock


class WireStockRepository:

    @staticmethod
    def get_query(db: Session):
        return db.query(WireStock).options(
            joinedload(WireStock.wire),
            joinedload(WireStock.supplier),
        )

    @staticmethod
    def create(db: Session, data: dict):
        try:
            stock = WireStock(**data)

            db.add(stock)
            db.commit()
            db.refresh(stock)

            return WireStockRepository.get_by_id(db, stock.id)

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_all(db: Session):
        return (
            WireStockRepository.get_query(db)
            .order_by(WireStock.id.desc())
            .all()
        )

    @staticmethod
    def get_by_id(db: Session, stock_id: int):
        return (
            WireStockRepository.get_query(db)
            .filter(WireStock.id == stock_id)
            .first()
        )

    @staticmethod
    def update(db: Session, stock: WireStock, data: dict):
        try:
            for key, value in data.items():
                setattr(stock, key, value)

            db.commit()
            db.refresh(stock)

            return WireStockRepository.get_by_id(db, stock.id)

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def delete(db: Session, stock: WireStock):
        try:
            db.delete(stock)
            db.commit()
            return True

        except Exception:
            db.rollback()
            raise