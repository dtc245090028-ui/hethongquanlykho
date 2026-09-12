from datetime import datetime, timezone

from app.extensions import db


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class SupplierOffer(db.Model):
    """Một lần nhà cung cấp chào giá cho hàng hóa."""

    __tablename__ = "supplier_offers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=False)
    goods_id = db.Column(db.Integer, db.ForeignKey("goods.id"), nullable=True)
    product_name = db.Column(db.String(200), nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    quantity_available = db.Column(db.Float, nullable=False, default=0.0)
    proposed_price = db.Column(db.Float, nullable=False)
    price_reason = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=utc_now, nullable=False)

    supplier = db.relationship("Supplier", back_populates="offers")
    goods = db.relationship("Goods")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "supplier_id": self.supplier_id,
            "goods_id": self.goods_id,
            "product_name": self.product_name,
            "unit": self.unit,
            "quantity_available": self.quantity_available,
            "proposed_price": self.proposed_price,
            "price_reason": self.price_reason,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }