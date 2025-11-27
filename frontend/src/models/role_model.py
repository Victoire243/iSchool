class RoleModel:
    """
    Role model representing a user role in the system.
    """

    def __init__(self, id_role: int, role_name: str, is_deleted: bool = False) -> None:
        self.id_role = id_role
        self.role_name = role_name
        self.is_deleted = is_deleted

    def to_dict(self) -> dict:
        """Convert the RoleModel instance to a dictionary."""
        return {
            "id_role": self.id_role,
            "role_name": self.role_name,
            "is_deleted": self.is_deleted,
        }

    def __repr__(self) -> str:
        return f"RoleModel(id_role={self.id_role}, role_name='{self.role_name}', is_deleted={self.is_deleted})"

    @classmethod
    def from_dict(cls, data: dict) -> "RoleModel":
        """Create a RoleModel instance from a dictionary."""
        return cls(
            id_role=data["id_role"],
            role_name=data["role_name"],
            is_deleted=data.get("is_deleted", False),
        )
