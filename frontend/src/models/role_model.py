class RoleModel:
    """
    Role model representing a user role in the system.
    """

    def __init__(self, id_role: int, role_name: str) -> None:
        self.id_role = id_role
        self.role_name = role_name

    def to_dict(self) -> dict:
        """Convert the RoleModel instance to a dictionary."""
        return {"id_role": self.id_role, "role_name": self.role_name}

    def __repr__(self) -> str:
        return f"RoleModel(id_role={self.id_role}, role_name='{self.role_name}')"

    @classmethod
    def from_dict(cls, data: dict) -> "RoleModel":
        """Create a RoleModel instance from a dictionary."""
        return cls(id_role=data["id_role"], role_name=data["role_name"])
