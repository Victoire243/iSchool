class StaffPaymentModel:
    """Model representing a staff payment record."""

    def __init__(
        self,
        id_staff_payment: int,
        staff_id: int,
        school_year_id: int,
        amount: float,
        payment_date: str,
        user_id: int,
        is_deleted: bool = False,
    ) -> None:
        self.id_staff_payment = id_staff_payment  # Primary key
        self.staff_id = staff_id  # Foreign key to StaffModel
        self.school_year_id = school_year_id  # Foreign key to SchoolYearModel
        self.amount = amount  # Payment amount
        self.payment_date = payment_date  # Date of payment
        self.user_id = user_id  # Foreign key to UserModel
        self.is_deleted = is_deleted

    def __repr__(self) -> str:
        return f"StaffPaymentModel(id_staff_payment={self.id_staff_payment}, staff_id={self.staff_id}, school_year_id={self.school_year_id}, amount={self.amount}, payment_date='{self.payment_date}', user_id={self.user_id}, is_deleted={self.is_deleted})"

    def to_dict(self) -> dict:
        """Convert the StaffPaymentModel instance to a dictionary."""
        return {
            "id_staff_payment": self.id_staff_payment,
            "staff_id": self.staff_id,
            "school_year_id": self.school_year_id,
            "amount": self.amount,
            "payment_date": self.payment_date,
            "user_id": self.user_id,
            "is_deleted": self.is_deleted,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "StaffPaymentModel":
        """Create a StaffPaymentModel instance from a dictionary."""
        return cls(
            id_staff_payment=data["id_staff_payment"],
            staff_id=data["staff_id"],
            school_year_id=data["school_year_id"],
            amount=data["amount"],
            payment_date=data["payment_date"],
            user_id=data["user_id"],
        )
