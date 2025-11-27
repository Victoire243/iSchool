class CashRegisterModel:
    """Model representing a cash register entry."""

    def __init__(
        self,
        id_cash: int,
        school_year_id: int,
        date: str,
        type: str,
        description: str,
        amount: float,
        user_id: int,
        is_deleted: bool = False,
    ) -> None:
        self.id_cash = id_cash  # Primary key
        self.school_year_id = school_year_id  # Foreign key to SchoolYearModel
        self.date = date  # Date of the cash register entry
        self.type = type  # Type of entry (e.g., "Entrée", "Sortie")
        self.description = description  # Description of the entry
        self.amount = amount  # Amount of money involved
        self.user_id = user_id  # Foreign key to UserModel
        self.is_deleted = is_deleted

    def __repr__(self) -> str:
        return f"CashRegisterModel(id_cash={self.id_cash}, school_year_id={self.school_year_id}, date='{self.date}', type='{self.type}', description='{self.description}', amount={self.amount}, user_id={self.user_id}, is_deleted={self.is_deleted})"

    def to_dict(self) -> dict:
        """Convert the CashRegisterModel instance to a dictionary."""
        return {
            "id_cash": self.id_cash,
            "school_year_id": self.school_year_id,
            "date": self.date,
            "type": self.type,
            "description": self.description,
            "amount": self.amount,
            "user_id": self.user_id,
            "is_deleted": self.is_deleted,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CashRegisterModel":
        """Create a CashRegisterModel instance from a dictionary."""
        return cls(
            id_cash=data["id_cash"],
            school_year_id=data["school_year_id"],
            date=data["date"],
            type=data["type"],
            description=data["description"],
            amount=data["amount"],
            user_id=data["user_id"],
        )
