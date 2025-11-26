class PaymentTypeModel:
    def __init__(
        self,
        id_payment_type: int,
        name: str,
        description: str,
        amount_defined: float,
        is_deleted: bool = False,
    ) -> None:
        self.id_payment_type = id_payment_type
        self.name = name
        self.description = (description,)
        self.amount_defined = amount_defined
        self.is_deleted = is_deleted

    def __repr__(self) -> str:
        return f"<PaymentType {self.name} ({self.amount_defined}) is_deleted={self.is_deleted}>"

    def to_dict(self) -> dict:
        return {
            "id_payment_type": self.id_payment_type,
            "name": self.name,
            "description": self.description,
            "amount_defined": self.amount_defined,
            "is_deleted": self.is_deleted,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "PaymentTypeModel":
        return cls(
            id_payment_type=data["id_payment_type"],
            name=data["name"],
            description=data["description"],
            amount_defined=data["amount_defined"],
            is_deleted=data.get("is_deleted", False),
        )
