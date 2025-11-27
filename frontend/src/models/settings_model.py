class SettingsModel:
    """Model representing application settings."""

    def __init__(
        self, id_settings: int, key: str, value: str, description: str
    ) -> None:
        self.id_settings = id_settings
        self.key = key
        self.value = value
        self.description = description

    def __repr__(self) -> str:
        return f"SettingsModel(id_settings={self.id_settings}, key='{self.key}', value='{self.value}')"

    def to_dict(self) -> dict:
        return {
            "id_settings": self.id_settings,
            "key": self.key,
            "value": self.value,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "SettingsModel":
        return cls(
            id_settings=data["id_settings"],
            key=data["key"],
            value=data["value"],
            description=data.get("description", ""),
        )
