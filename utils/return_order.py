class ReturnOrder:
    def __init__(
        self,
        order_id: int,
        price: float,
        name: str,
        receipt_mobile: int,
        attend_mobile: int,
        address: str,
    ):
        self.order_id = order_id
        self.order_id_20 = int(str(self.order_id)[:20])
        self.price = price
        self.name = name
        self.receipt_mobile = receipt_mobile
        self.attend_mobile = attend_mobile
        self.address = address

    def __repr__(self) -> str:
        return (
            f"order_id={self.order_id}, order_id_20={self.order_id_20}, price={self.price}, "
            f"name={self.name}, receipt_mobile={self.receipt_mobile}, "
            f"attend_mobile={self.attend_mobile}, address={self.address}"
        )
