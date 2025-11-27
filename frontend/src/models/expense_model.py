class ExpenseModel:
    """Model representing an expense record."""

    def __init__(
        self,
        id_expense: int,
        school_year_id: int,
        expense_date: str,
        description: str,
        amount: float,
        user_id: int,
        is_deleted: bool = False,
    ) -> None:
        self.id_expense = id_expense  # Primary key
        self.school_year_id = school_year_id  # Foreign key to SchoolYearModel
        self.expense_date = expense_date  # Date of the expense
        self.description = description  # Description of the expense
        self.amount = amount  # Amount of the expense
        self.user_id = user_id  # Foreign key to UserModel
        self.is_deleted = is_deleted

    def __repr__(self) -> str:
        return f"ExpenseModel(id_expense={self.id_expense}, school_year_id={self.school_year_id}, expense_date='{self.expense_date}', description='{self.description}', amount={self.amount}, user_id={self.user_id}, is_deleted={self.is_deleted})"

    def to_dict(self) -> dict:
        """Convert the ExpenseModel instance to a dictionary."""
        return {
            "id_expense": self.id_expense,
            "school_year_id": self.school_year_id,
            "expense_date": self.expense_date,
            "description": self.description,
            "amount": self.amount,
            "user_id": self.user_id,
            "is_deleted": self.is_deleted,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ExpenseModel":
        """Create an ExpenseModel instance from a dictionary."""
        return cls(
            id_expense=data["id_expense"],
            school_year_id=data["school_year_id"],
            expense_date=data["expense_date"],
            description=data["description"],
            amount=data["amount"],
            user_id=data["user_id"],
        )
