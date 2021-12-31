from datetime import datetime


class Order:
    def __init__(
        self,
        order_id: int,
        price: float,
        order_time: datetime,
        name: str,
        receipt_mobile: int,
        attend_mobile: int,
        address: str,
        notes: str,
    ):
        self.order_id = order_id
        self.order_id_20 = int(str(self.order_id)[:20])
        self.price = price
        self.order_time = order_time
        self.name = name
        self.receipt_mobile = receipt_mobile
        self.attend_mobile = attend_mobile
        self.address = address
        self.notes = notes

    def __repr__(self) -> str:
        return (
            f"order_id={self.order_id}, order_id_20={self.order_id_20}, price={self.price}, "
            f"order_time={self.order_time}, name={self.name}, receipt_mobile={self.receipt_mobile}, "
            f"attend_mobile={self.attend_mobile}, address={self.address}, notes={self.notes}"
        )
