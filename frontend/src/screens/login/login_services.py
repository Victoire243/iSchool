from models import UserModel


class LoginServices:
    def __init__(self) -> None:
        pass

    def authenticate(self, username: str, password: str) -> UserModel | None:
        # Placeholder authentication logic
        if username == "admin" and password == "admin":
            return UserModel(
                id_user=1,
                username="admin",
                email="admin@example.com",
                password="admin",
                role_id=1,
            )
        return None
