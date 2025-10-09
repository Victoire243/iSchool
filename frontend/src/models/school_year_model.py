class SchoolYearModel:
    """Model representing a school year."""

    def __init__(
        self,
        id_school_year: int,
        name: str,  # e.g., "2023-2024"
        start_date: str,
        end_date: str,
        is_active: bool,
    ) -> None:
        self.id_school_year = id_school_year  # Primary key
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.is_active = is_active

    def __repr__(self) -> str:
        return f"SchoolYearModel(id_school_year={self.id_school_year}, name='{self.name}', start_date='{self.start_date}', end_date='{self.end_date}', is_active={self.is_active})"

    def to_dict(self) -> dict:
        """Convert the SchoolYearModel instance to a dictionary."""
        return {
            "id_school_year": self.id_school_year,
            "name": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "is_active": self.is_active,
        }
