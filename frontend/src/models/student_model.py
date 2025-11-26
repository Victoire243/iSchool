class StudentModel:
    """Model representing a student with relevant attributes."""

    def __init__(
        self,
        id_student: int,
        first_name: str,  # in french "prénom"
        last_name: str,  # in french "nom de famille" ou "nom"
        surname: str,  # in french "post-nom"
        gender: str,
        date_of_birth: str,
        address: str,
        parent_contact: str,
        is_deleted: bool = False,
    ) -> None:
        self.id_student = id_student
        self.first_name = first_name
        self.last_name = last_name
        self.surname = surname
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.address = address
        self.parent_contact = parent_contact
        self.is_deleted = is_deleted

    def __repr__(self) -> str:
        return f"StudentModel(id_student={self.id_student}, first_name='{self.first_name}', last_name='{self.last_name}', surname='{self.surname}', gender='{self.gender}', date_of_birth='{self.date_of_birth}', address='{self.address}', parent_contact='{self.parent_contact}', is_deleted={self.is_deleted})"

    def to_dict(self) -> dict:
        """Convert the StudentModel instance to a dictionary."""
        return {
            "id_student": self.id_student,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "surname": self.surname,
            "gender": self.gender,
            "date_of_birth": self.date_of_birth,
            "address": self.address,
            "parent_contact": self.parent_contact,
            "is_deleted": self.is_deleted,
        }
