class PaymentModel:
    """Represents a payment record in the system."""

    def __init__(
        self,
        id_payment: int,
        student_id: int,
        school_year_id: int,
        payment_type_id: int,
        amount: float,
        payment_date: str,
        user_id: int,
        is_deleted: bool = False,
    ) -> None:
        self.id_payment = id_payment  # Primary key
        self.student_id = student_id  # Foreign key to StudentModel
        self.school_year_id = school_year_id  # Foreign key to SchoolYearModel
        self.payment_type_id = payment_type_id  # Foreign key to PaymentTypeModel
        self.amount = amount  # Payment amount
        self.payment_date = payment_date  # Date of payment
        self.user_id = user_id  # Foreign key to UserModel
        self.is_deleted = is_deleted

    def __repr__(self) -> str:
        return f"PaymentModel(id_payment={self.id_payment}, student_id={self.student_id}, school_year_id={self.school_year_id}, payment_type_id={self.payment_type_id}, amount={self.amount}, payment_date='{self.payment_date}', user_id={self.user_id}, is_deleted={self.is_deleted})"

    def to_dict(self) -> dict:
        """Convert the PaymentModel instance to a dictionary."""
        return {
            "id_payment": self.id_payment,
            "student_id": self.student_id,
            "school_year_id": self.school_year_id,
            "payment_type_id": self.payment_type_id,
            "amount": self.amount,
            "payment_date": self.payment_date,
            "user_id": self.user_id,
            "is_deleted": self.is_deleted,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "PaymentModel":
        """Create a PaymentModel instance from a dictionary."""
        return cls(
            id_payment=data["id_payment"],
            student_id=data["student_id"],
            school_year_id=data["school_year_id"],
            payment_type_id=data["payment_type_id"],
            amount=data["amount"],
            payment_date=data["payment_date"],
            user_id=data["user_id"],
        )
