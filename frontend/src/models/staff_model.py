class StaffModel:
    """Model representing a staff member in the school management system."""

    def __init__(
        self,
        id_staff: int,
        first_name: str,
        last_name: str,
        position: str,
        hire_date: str,
        salary_base: float,
    ) -> None:
        self.id_staff = id_staff  # Primary key
        self.first_name = first_name  # Staff member's first name
        self.last_name = last_name  # Staff member's last name
        self.position = position  # Position (e.g., "Enseignant", "Comptable")
        self.hire_date = hire_date  # Date of hire
        self.salary_base = salary_base  # Base salary

    def __repr__(self) -> str:
        return f"StaffModel(id_staff={self.id_staff}, first_name='{self.first_name}', last_name='{self.last_name}', position='{self.position}', hire_date='{self.hire_date}', salary_base={self.salary_base})"

    def to_dict(self) -> dict:
        """Convert the StaffModel instance to a dictionary."""
        return {
            "id_staff": self.id_staff,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "position": self.position,
            "hire_date": self.hire_date,
            "salary_base": self.salary_base,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "StaffModel":
        """Create a StaffModel instance from a dictionary."""
        return cls(
            id_staff=data["id_staff"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            position=data["position"],
            hire_date=data["hire_date"],
            salary_base=data["salary_base"],
        )
