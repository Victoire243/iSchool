"""
Fee Model
=========
Modèle pour gérer les types de frais scolaires avec leur périodicité.
"""


class FeeModel:
    """
    Modèle représentant un type de frais scolaire.

    Périodicité:
    - 'monthly': Frais mensuels
    - 'quarterly': Frais trimestriels
    - 'semester': Frais semestriels
    - 'annual': Frais annuels
    - 'one_time': Frais unique sans date fixe
    """

    def __init__(
        self,
        id_fee: int,
        name: str,
        description: str,
        amount: float,
        periodicity: str,  # 'monthly', 'quarterly', 'semester', 'annual', 'one_time'
        is_active: bool = True,
        is_deleted: bool = False,
    ) -> None:
        self.id_fee = id_fee
        self.name = name
        self.description = description
        self.amount = amount
        self.periodicity = periodicity
        self.is_active = is_active
        self.is_deleted = is_deleted

    def __repr__(self) -> str:
        return f"<Fee {self.name} ({self.amount}) - {self.periodicity}>"

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id_fee": self.id_fee,
            "name": self.name,
            "description": self.description,
            "amount": self.amount,
            "periodicity": self.periodicity,
            "is_active": self.is_active,
            "is_deleted": self.is_deleted,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "FeeModel":
        """Create from dictionary"""
        return cls(
            id_fee=data["id_fee"],
            name=data["name"],
            description=data["description"],
            amount=data["amount"],
            periodicity=data["periodicity"],
            is_active=data.get("is_active", True),
            is_deleted=data.get("is_deleted", False),
        )

    def get_periodicity_display(self) -> str:
        """Return human-readable periodicity"""
        periodicity_map = {
            "monthly": "Mensuel",
            "quarterly": "Trimestriel",
            "semester": "Semestriel",
            "annual": "Annuel",
            "one_time": "Paiement unique",
        }
        return periodicity_map.get(self.periodicity, self.periodicity)
