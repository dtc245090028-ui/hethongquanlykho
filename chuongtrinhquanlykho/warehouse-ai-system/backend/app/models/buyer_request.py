from datetime import datetime, timezone

from app.extensions import db


def utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


class BuyerRequest(db.Model):
    __tablename__ = "buyer_requests"

    id = db.Column(db.Integer, primary_key=True)
    buyer_name = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Enum("chờ xử lý", "đã tạo đơn", "đã hủy", name="buyer_request_status"), nullable=False, default="chờ xử lý")
    created_at = db.Column(db.DateTime, default=utc_now, nullable=False)
    purchase_order_id = db.Column(db.Integer, db.ForeignKey("purchase_orders.id"), nullable=True)

    items = db.relationship("BuyerRequestItem", cascade="all, delete-orphan", back_populates="request")
    purchase_order = db.relationship("PurchaseOrder")

    def to_dict(self, include_items=False):
        data = {"id": self.id, "buyer_name": self.buyer_name, "status": self.status, "created_at": self.created_at.isoformat() if self.created_at else None, "purchase_order_id": self.purchase_order_id}
        if include_items:
            data["items"] = [item.to_dict() for item in self.items]
        return data


class BuyerRequestItem(db.Model):
    __tablename__ = "buyer_request_items"

    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey("buyer_requests.id"), nullable=False)
    goods_id = db.Column(db.Integer, db.ForeignKey("goods.id"), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False, default=0.0)
    request = db.relationship("BuyerRequest", back_populates="items")
    goods = db.relationship("Goods")

    def to_dict(self):
        total = self.quantity * self.unit_price
        return {"id": self.id, "goods_id": self.goods_id, "goods_name": self.goods.name if self.goods else None, "unit": self.goods.unit if self.goods else None, "quantity": self.quantity, "unit_price": self.unit_price, "total_amount": total}