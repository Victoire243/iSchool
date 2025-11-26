class EnrollmentModel:
    """Model representing an enrollment record in the school management system."""

    def __init__(
        self,
        id_enrollment: int,
        student_id: int,
        classroom_id: int,
        school_year_id: int,
        status: str,
        is_deleted: bool = False,
    ) -> None:
        self.id_enrollment = id_enrollment  # Primary key
        self.student_id = student_id  # Foreign key to StudentModel
        self.classroom_id = classroom_id  # Foreign key to ClassroomModel
        self.school_year_id = school_year_id  # Foreign key to SchoolYearModel
        self.status = status  # e.g., "Admis", "Redoublant", "Abandonné"
        self.is_deleted = is_deleted

    def __repr__(self) -> str:
        return f"EnrollmentModel(id_enrollment={self.id_enrollment}, student_id={self.student_id}, classroom_id={self.classroom_id}, school_year_id={self.school_year_id}, status='{self.status}', is_deleted={self.is_deleted})"

    def to_dict(self) -> dict:
        """Convert the EnrollmentModel instance to a dictionary."""
        return {
            "id_enrollment": self.id_enrollment,
            "student_id": self.student_id,
            "classroom_id": self.classroom_id,
            "school_year_id": self.school_year_id,
            "status": self.status,
            "is_deleted": self.is_deleted,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "EnrollmentModel":
        """Create an EnrollmentModel instance from a dictionary."""
        return cls(
            id_enrollment=data["id_enrollment"],
            student_id=data["student_id"],
            classroom_id=data["classroom_id"],
            school_year_id=data["school_year_id"],
            status=data["status"],
        )
