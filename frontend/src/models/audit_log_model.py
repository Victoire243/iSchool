class AuditLogModel:
    """Model representing an audit log entry."""

    def __init__(
        self,
        id_log: int,
        user_id: int,
        action: str,
        table_name: str,
        record_id: int,
        timestamp: str,
        details: str,
    ) -> None:
        self.id_log = id_log
        self.user_id = user_id
        self.action = action
        self.table_name = table_name
        self.record_id = record_id
        self.timestamp = timestamp
        self.details = details

    def __repr__(self) -> str:
        return f"AuditLogModel(id_log={self.id_log}, action='{self.action}', table='{self.table_name}')"

    def to_dict(self) -> dict:
        return {
            "id_log": self.id_log,
            "user_id": self.user_id,
            "action": self.action,
            "table_name": self.table_name,
            "record_id": self.record_id,
            "timestamp": self.timestamp,
            "details": self.details,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AuditLogModel":
        return cls(
            id_log=data["id_log"],
            user_id=data["user_id"],
            action=data["action"],
            table_name=data["table_name"],
            record_id=data["record_id"],
            timestamp=data["timestamp"],
            details=data.get("details", ""),
        )
