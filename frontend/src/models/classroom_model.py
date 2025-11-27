class ClassroomModel:
    """A model representing a classroom in the system."""

    def __init__(
        self, id_classroom: int, name: str, level: str, is_deleted: bool = False
    ) -> None:
        self.id_classroom = id_classroom  # Primary key
        self.name = name  # e.g., "6ème A"
        self.level = level  # e.g., "Primaire", "Secondaire"
        self.is_deleted = is_deleted

    def __repr__(self) -> str:
        return f"<Classroom {self.name} ({self.level}) is_deleted={self.is_deleted}>"

    def to_dict(self) -> dict:
        return {
            "id_classroom": self.id_classroom,
            "name": self.name,
            "level": self.level,
            "is_deleted": self.is_deleted,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ClassroomModel":
        return cls(
            id_classroom=data["id_classroom"],
            name=data["name"],
            level=data["level"],
            is_deleted=data.get("is_deleted", False),
        )
