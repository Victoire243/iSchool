class PaymentTypeModel:
    def __init__(
        self,
        id_payment_type: int,
        name: str,
        description: str,
        amount_defined: float,
    ) -> None:
        self.id_payment_type = id_payment_type
        self.name = name
        self.description = (description,)
        self.amount_defined = amount_defined

    def __repr__(self) -> str:
        return f"<PaymentType {self.name} ({self.amount_defined})>"

    def to_dict(self) -> dict:
        return {
            "id_payment_type": self.id_payment_type,
            "name": self.name,
            "description": self.description,
            "amount_defined": self.amount_defined,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "PaymentTypeModel":
        return cls(
            id_payment_type=data["id_payment_type"],
            name=data["name"],
            description=data["description"],
            amount_defined=data["amount_defined"],
        )
