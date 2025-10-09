class UserModel:
    """
    User model representing a user in the system.
    """

    def __init__(
        self,
        id_user: int,
        username: str,
        email: str,
        password: str,
        role_id: int,
    ) -> None:
        self.id_user = id_user  # Primary key
        self.username = username
        self.email = email
        self.password = password
        self.role_id = role_id  # Foreign key to RoleModel

    def to_dict(self) -> dict:
        """Convert the UserModel instance to a dictionary."""
        return {
            "id_user": self.id_user,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "role_id": self.role_id,
        }

    def __repr__(self) -> str:
        return f"UserModel(id_user={self.id_user}, username='{self.username}', email='{self.email}', role_id={self.role_id})"

    @classmethod
    def from_dict(cls, data: dict) -> "UserModel":
        """Create a UserModel instance from a dictionary."""
        return cls(
            id_user=data["id_user"],
            username=data["username"],
            email=data["email"],
            password=data["password"],
            role_id=data["role_id"],
        )
