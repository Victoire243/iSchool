# Génération de données fictives (selon les modèles) pour les tests et le développement.

from __future__ import annotations

import random
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

from faker import Faker

# Import des modèles
from models.cash_register_model import CashRegisterModel
from models.classroom_model import ClassroomModel
from models.enrollment_model import EnrollmentModel
from models.expense_model import ExpenseModel
from models.payment_model import PaymentModel
from models.payment_type_model import PaymentTypeModel
from models.role_model import RoleModel
from models.school_year_model import SchoolYearModel
from models.staff_model import StaffModel
from models.staff_payment_model import StaffPaymentModel
from models.student_model import StudentModel
from models.user_model import UserModel


FAKE_DB_PATH = Path(__file__).resolve().parent / "fake_api.db"


@dataclass(frozen=True)
class FakeDataset:
    roles: List[dict]
    users: List[dict]
    school_years: List[dict]
    classrooms: List[dict]
    students: List[dict]
    enrollments: List[dict]
    payment_types: List[dict]
    payments: List[dict]
    expenses: List[dict]
    staff: List[dict]
    staff_payments: List[dict]
    cash_register: List[dict]


class FakeDataFactory:
    """Fabrique responsable de générer des jeux de données cohérents."""

    def __init__(self, seed: int | None = None) -> None:
        self._faker = Faker("fr_FR")
        self._random = random.Random(seed)
        if seed is not None:
            Faker.seed(seed)
            self._faker.seed_instance(seed)

    # -- Public API ------------------------------------------------------------------
    def build_dataset(self) -> FakeDataset:
        roles = self._build_roles()
        users = self._build_users(roles)
        school_years = self._build_school_years()
        classrooms = self._build_classrooms()
        students = self._build_students()
        enrollments = self._build_enrollments(students, classrooms, school_years)
        payment_types = self._build_payment_types()
        payments = self._build_payments(students, school_years, payment_types, users)
        expenses = self._build_expenses(school_years, users)
        staff = self._build_staff()
        staff_payments = self._build_staff_payments(staff, school_years, users)
        cash_register = self._build_cash_register(payments, expenses)

        return FakeDataset(
            roles=[role.to_dict() for role in roles],
            users=[user.to_dict() for user in users],
            school_years=[school_year.to_dict() for school_year in school_years],
            classrooms=[classroom.to_dict() for classroom in classrooms],
            students=[student.to_dict() for student in students],
            enrollments=[enrollment.to_dict() for enrollment in enrollments],
            payment_types=[_sanitize_payment_type(pt) for pt in payment_types],
            payments=[payment.to_dict() for payment in payments],
            expenses=[expense.to_dict() for expense in expenses],
            staff=[member.to_dict() for member in staff],
            staff_payments=[
                staff_payment.to_dict() for staff_payment in staff_payments
            ],
            cash_register=[entry.to_dict() for entry in cash_register],
        )

    # -- Construction helpers -------------------------------------------------------
    def _build_roles(self) -> List[RoleModel]:
        role_names = [
            "Administrateur",
            "Comptable",
            "Secrétaire",
            "Enseignant",
            "Surveillant",
        ]
        return [
            RoleModel(id_role=index + 1, role_name=name)
            for index, name in enumerate(role_names)
        ]

    def _build_users(
        self, roles: Sequence[RoleModel], count: int = 8
    ) -> List[UserModel]:
        users: List[UserModel] = []
        for identifier in range(1, count + 1):
            role = self._random.choice(list(roles))
            full_name = self._faker.unique.name()
            username = full_name.lower().replace(" ", ".")
            users.append(
                UserModel(
                    id_user=identifier,
                    username=username,
                    email=f"{username}@school.test",
                    password=self._faker.password(length=12),
                    role_id=role.id_role,
                )
            )
        return users

    def _build_school_years(self, total: int = 3) -> List[SchoolYearModel]:
        current_year = datetime.now().year
        school_years: List[SchoolYearModel] = []
        for index in range(total):
            start = datetime(year=current_year - (total - index), month=9, day=1)
            end = start + timedelta(days=365)
            label = f"{start.year}-{end.year}"
            school_years.append(
                SchoolYearModel(
                    id_school_year=index + 1,
                    name=label,
                    start_date=start.strftime("%Y-%m-%d"),
                    end_date=end.strftime("%Y-%m-%d"),
                    is_active=index == total - 1,
                )
            )
        return school_years

    def _build_classrooms(self) -> List[ClassroomModel]:
        levels = [
            ("1ère A", "Primaire"),
            ("2ème A", "Primaire"),
            ("3ème B", "Primaire"),
            ("4ème C", "Secondaire"),
            ("5ème Scientifique", "Secondaire"),
            ("6ème Informatique", "Secondaire"),
        ]
        return [
            ClassroomModel(id_classroom=index + 1, name=name, level=level)
            for index, (name, level) in enumerate(levels)
        ]

    def _build_students(self, count: int = 24) -> List[StudentModel]:
        students: List[StudentModel] = []
        for identifier in range(1, count + 1):
            gender = self._random.choice(["Masculin", "Féminin"])
            birth_date = self._faker.date_of_birth(minimum_age=9, maximum_age=18)
            students.append(
                StudentModel(
                    id_student=identifier,
                    first_name=(
                        self._faker.first_name_male()
                        if gender == "Masculin"
                        else self._faker.first_name_female()
                    ),
                    last_name=self._faker.last_name(),
                    surname=self._faker.last_name(),
                    gender=gender,
                    date_of_birth=birth_date.strftime("%Y-%m-%d"),
                    address=self._faker.address().replace("\n", ", "),
                    parent_contact=self._faker.phone_number(),
                )
            )
        return students

    def _build_enrollments(
        self,
        students: Sequence[StudentModel],
        classrooms: Sequence[ClassroomModel],
        school_years: Sequence[SchoolYearModel],
    ) -> List[EnrollmentModel]:
        enrollments: List[EnrollmentModel] = []
        statuses = ["Admis", "Redoublant", "Abandonné"]
        active_school_year = max(school_years, key=lambda year: year.id_school_year)
        for identifier, student in enumerate(students, start=1):
            classroom = self._random.choice(list(classrooms))
            status = self._random.choices(statuses, weights=[0.7, 0.2, 0.1], k=1)[0]
            enrollments.append(
                EnrollmentModel(
                    id_enrollment=identifier,
                    student_id=student.id_student,
                    classroom_id=classroom.id_classroom,
                    school_year_id=active_school_year.id_school_year,
                    status=status,
                )
            )
        return enrollments

    def _build_payment_types(self) -> List[PaymentTypeModel]:
        payment_definitions = [
            ("Minerval", "Paiement principal des frais de scolarité", 250.0),
            ("Transport", "Frais de transport scolaire", 60.0),
            ("Cantine", "Forfait cantine mensuel", 45.0),
            ("Bibliothèque", "Carte bibliothèque annuelle", 15.0),
        ]
        payment_types: List[PaymentTypeModel] = []
        for identifier, (name, description, amount) in enumerate(
            payment_definitions, start=1
        ):
            payment_types.append(
                PaymentTypeModel(
                    id_payment_type=identifier,
                    name=name,
                    description=description,
                    amount_defined=amount,
                )
            )
        return payment_types

    def _build_payments(
        self,
        students: Sequence[StudentModel],
        school_years: Sequence[SchoolYearModel],
        payment_types: Sequence[PaymentTypeModel],
        users: Sequence[UserModel],
    ) -> List[PaymentModel]:
        payments: List[PaymentModel] = []
        identifier = 1
        active_year = max(school_years, key=lambda year: year.id_school_year)
        for student in students:
            payment_count = self._random.randint(1, 3)
            for _ in range(payment_count):
                payment_type = self._random.choice(list(payment_types))
                date = datetime.now() - timedelta(days=self._random.randint(0, 120))
                payments.append(
                    PaymentModel(
                        id_payment=identifier,
                        student_id=student.id_student,
                        school_year_id=active_year.id_school_year,
                        payment_type_id=payment_type.id_payment_type,
                        amount=round(
                            payment_type.amount_defined
                            * self._random.uniform(0.8, 1.2),
                            2,
                        ),
                        payment_date=date.strftime("%Y-%m-%d"),
                        user_id=self._random.choice(list(users)).id_user,
                    )
                )
                identifier += 1
        return payments

    def _build_expenses(
        self,
        school_years: Sequence[SchoolYearModel],
        users: Sequence[UserModel],
        count: int = 18,
    ) -> List[ExpenseModel]:
        descriptors = [
            "Achat de matériel pédagogique",
            "Maintenance des bâtiments",
            "Achat de fournitures de bureau",
            "Organisation voyage scolaire",
            "Honoraires consultants",
            "Frais administratifs",
        ]
        expenses: List[ExpenseModel] = []
        active_year = max(school_years, key=lambda year: year.id_school_year)
        for identifier in range(1, count + 1):
            date = datetime.now() - timedelta(days=self._random.randint(0, 180))
            expenses.append(
                ExpenseModel(
                    id_expense=identifier,
                    school_year_id=active_year.id_school_year,
                    expense_date=date.strftime("%Y-%m-%d"),
                    description=self._random.choice(descriptors),
                    amount=round(self._random.uniform(25.0, 500.0), 2),
                    user_id=self._random.choice(list(users)).id_user,
                )
            )
        return expenses

    def _build_staff(self, count: int = 12) -> List[StaffModel]:
        positions = [
            "Enseignant",
            "Educateur",
            "Comptable",
            "Surveillant",
            "Bibliothécaire",
            "Responsable informatique",
        ]
        staff_members: List[StaffModel] = []
        for identifier in range(1, count + 1):
            hire_date = datetime.now() - timedelta(days=self._random.randint(30, 3650))
            staff_members.append(
                StaffModel(
                    id_staff=identifier,
                    first_name=self._faker.first_name(),
                    last_name=self._faker.last_name(),
                    position=self._random.choice(positions),
                    hire_date=hire_date.strftime("%Y-%m-%d"),
                    salary_base=round(self._random.uniform(350.0, 950.0), 2),
                )
            )
        return staff_members

    def _build_staff_payments(
        self,
        staff: Sequence[StaffModel],
        school_years: Sequence[SchoolYearModel],
        users: Sequence[UserModel],
    ) -> List[StaffPaymentModel]:
        payments: List[StaffPaymentModel] = []
        identifier = 1
        active_year = max(school_years, key=lambda year: year.id_school_year)
        for member in staff:
            for _ in range(self._random.randint(1, 4)):
                pay_date = datetime.now() - timedelta(days=self._random.randint(0, 90))
                payments.append(
                    StaffPaymentModel(
                        id_staff_payment=identifier,
                        staff_id=member.id_staff,
                        school_year_id=active_year.id_school_year,
                        amount=round(
                            member.salary_base * self._random.uniform(0.9, 1.1), 2
                        ),
                        payment_date=pay_date.strftime("%Y-%m-%d"),
                        user_id=self._random.choice(list(users)).id_user,
                    )
                )
                identifier += 1
        return payments

    def _build_cash_register(
        self,
        payments: Sequence[PaymentModel],
        expenses: Sequence[ExpenseModel],
    ) -> List[CashRegisterModel]:
        entries: List[CashRegisterModel] = []
        identifier = 1
        for payment in payments:
            entries.append(
                CashRegisterModel(
                    id_cash=identifier,
                    school_year_id=payment.school_year_id,
                    date=payment.payment_date,
                    type="Entrée",
                    description=f"Paiement élève #{payment.student_id}",
                    amount=payment.amount,
                    user_id=payment.user_id,
                )
            )
            identifier += 1
        for expense in expenses:
            entries.append(
                CashRegisterModel(
                    id_cash=identifier,
                    school_year_id=expense.school_year_id,
                    date=expense.expense_date,
                    type="Sortie",
                    description=expense.description,
                    amount=expense.amount,
                    user_id=expense.user_id,
                )
            )
            identifier += 1
        return entries


# -- Base de données SQLite ---------------------------------------------------------


def initialize_fake_database(
    db_path: Path | str | None = None, seed: int | None = None
) -> Path:
    """Crée ou reconstruit une base de données SQLite remplie de données fictives."""

    target_path = Path(db_path) if db_path else FAKE_DB_PATH
    target_path.parent.mkdir(parents=True, exist_ok=True)

    dataset = FakeDataFactory(seed=seed).build_dataset()

    with sqlite3.connect(target_path) as connection:
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys = OFF;")
        _recreate_schema(cursor)
        _insert_dataset(cursor, dataset)
        connection.commit()

    return target_path


def _recreate_schema(cursor: sqlite3.Cursor) -> None:
    """Supprime les tables existantes puis recrée le schéma minimal."""

    schema_statements = [
        "DROP TABLE IF EXISTS cash_register;",
        "DROP TABLE IF EXISTS staff_payments;",
        "DROP TABLE IF EXISTS staff;",
        "DROP TABLE IF EXISTS expenses;",
        "DROP TABLE IF EXISTS payments;",
        "DROP TABLE IF EXISTS payment_types;",
        "DROP TABLE IF EXISTS enrollments;",
        "DROP TABLE IF EXISTS students;",
        "DROP TABLE IF EXISTS classrooms;",
        "DROP TABLE IF EXISTS school_years;",
        "DROP TABLE IF EXISTS users;",
        "DROP TABLE IF EXISTS roles;",
        "DROP TABLE IF EXISTS settings;",
        "DROP TABLE IF EXISTS audit_logs;",
        "CREATE TABLE roles (id_role INTEGER PRIMARY KEY, role_name TEXT NOT NULL, is_deleted INTEGER DEFAULT 0);",
        "CREATE TABLE users (id_user INTEGER PRIMARY KEY, username TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL, role_id INTEGER NOT NULL, is_deleted INTEGER DEFAULT 0, FOREIGN KEY(role_id) REFERENCES roles(id_role));",
        "CREATE TABLE school_years (id_school_year INTEGER PRIMARY KEY, name TEXT NOT NULL, start_date TEXT NOT NULL, end_date TEXT NOT NULL, is_active INTEGER NOT NULL, is_deleted INTEGER DEFAULT 0);",
        "CREATE TABLE classrooms (id_classroom INTEGER PRIMARY KEY, name TEXT NOT NULL, level TEXT NOT NULL, is_deleted INTEGER DEFAULT 0);",
        "CREATE TABLE students (id_student INTEGER PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL, surname TEXT NOT NULL, gender TEXT NOT NULL, date_of_birth TEXT NOT NULL, address TEXT NOT NULL, parent_contact TEXT NOT NULL, is_deleted INTEGER DEFAULT 0);",
        "CREATE TABLE enrollments (id_enrollment INTEGER PRIMARY KEY, student_id INTEGER NOT NULL, classroom_id INTEGER NOT NULL, school_year_id INTEGER NOT NULL, status TEXT NOT NULL, is_deleted INTEGER DEFAULT 0, FOREIGN KEY(student_id) REFERENCES students(id_student), FOREIGN KEY(classroom_id) REFERENCES classrooms(id_classroom), FOREIGN KEY(school_year_id) REFERENCES school_years(id_school_year));",
        "CREATE TABLE payment_types (id_payment_type INTEGER PRIMARY KEY, name TEXT NOT NULL, description TEXT NOT NULL, amount_defined REAL NOT NULL, is_deleted INTEGER DEFAULT 0);",
        "CREATE TABLE payments (id_payment INTEGER PRIMARY KEY, student_id INTEGER NOT NULL, school_year_id INTEGER NOT NULL, payment_type_id INTEGER NOT NULL, amount REAL NOT NULL, payment_date TEXT NOT NULL, user_id INTEGER NOT NULL, is_deleted INTEGER DEFAULT 0, FOREIGN KEY(student_id) REFERENCES students(id_student), FOREIGN KEY(school_year_id) REFERENCES school_years(id_school_year), FOREIGN KEY(payment_type_id) REFERENCES payment_types(id_payment_type), FOREIGN KEY(user_id) REFERENCES users(id_user));",
        "CREATE TABLE expenses (id_expense INTEGER PRIMARY KEY, school_year_id INTEGER NOT NULL, expense_date TEXT NOT NULL, description TEXT NOT NULL, amount REAL NOT NULL, user_id INTEGER NOT NULL, is_deleted INTEGER DEFAULT 0, FOREIGN KEY(school_year_id) REFERENCES school_years(id_school_year), FOREIGN KEY(user_id) REFERENCES users(id_user));",
        "CREATE TABLE staff (id_staff INTEGER PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL, position TEXT NOT NULL, hire_date TEXT NOT NULL, salary_base REAL NOT NULL, is_deleted INTEGER DEFAULT 0);",
        "CREATE TABLE staff_payments (id_staff_payment INTEGER PRIMARY KEY, staff_id INTEGER NOT NULL, school_year_id INTEGER NOT NULL, amount REAL NOT NULL, payment_date TEXT NOT NULL, user_id INTEGER NOT NULL, is_deleted INTEGER DEFAULT 0, FOREIGN KEY(staff_id) REFERENCES staff(id_staff), FOREIGN KEY(school_year_id) REFERENCES school_years(id_school_year), FOREIGN KEY(user_id) REFERENCES users(id_user));",
        "CREATE TABLE cash_register (id_cash INTEGER PRIMARY KEY, school_year_id INTEGER NOT NULL, date TEXT NOT NULL, type TEXT NOT NULL, description TEXT NOT NULL, amount REAL NOT NULL, user_id INTEGER NOT NULL, is_deleted INTEGER DEFAULT 0, FOREIGN KEY(school_year_id) REFERENCES school_years(id_school_year), FOREIGN KEY(user_id) REFERENCES users(id_user));",
        "CREATE TABLE settings (id_settings INTEGER PRIMARY KEY, key TEXT NOT NULL UNIQUE, value TEXT NOT NULL, description TEXT);",
        "CREATE TABLE audit_logs (id_log INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, action TEXT NOT NULL, table_name TEXT NOT NULL, record_id INTEGER NOT NULL, timestamp TEXT NOT NULL, details TEXT, FOREIGN KEY(user_id) REFERENCES users(id_user));",
    ]
    for statement in schema_statements:
        cursor.execute(statement)


def _insert_dataset(cursor: sqlite3.Cursor, dataset: FakeDataset) -> None:
    table_columns: Dict[str, Sequence[str]] = {
        "roles": ("id_role", "role_name"),
        "users": ("id_user", "username", "email", "password", "role_id"),
        "school_years": (
            "id_school_year",
            "name",
            "start_date",
            "end_date",
            "is_active",
        ),
        "classrooms": ("id_classroom", "name", "level"),
        "students": (
            "id_student",
            "first_name",
            "last_name",
            "surname",
            "gender",
            "date_of_birth",
            "address",
            "parent_contact",
        ),
        "enrollments": (
            "id_enrollment",
            "student_id",
            "classroom_id",
            "school_year_id",
            "status",
        ),
        "payment_types": (
            "id_payment_type",
            "name",
            "description",
            "amount_defined",
        ),
        "payments": (
            "id_payment",
            "student_id",
            "school_year_id",
            "payment_type_id",
            "amount",
            "payment_date",
            "user_id",
        ),
        "expenses": (
            "id_expense",
            "school_year_id",
            "expense_date",
            "description",
            "amount",
            "user_id",
        ),
        "staff": (
            "id_staff",
            "first_name",
            "last_name",
            "position",
            "hire_date",
            "salary_base",
        ),
        "staff_payments": (
            "id_staff_payment",
            "staff_id",
            "school_year_id",
            "amount",
            "payment_date",
            "user_id",
        ),
        "cash_register": (
            "id_cash",
            "school_year_id",
            "date",
            "type",
            "description",
            "amount",
            "user_id",
        ),
    }

    iterable_dataset: Dict[str, Iterable[dict]] = dataset.__dict__

    insert_order = [
        "roles",
        "users",
        "school_years",
        "classrooms",
        "students",
        "payment_types",
        "enrollments",
        "payments",
        "expenses",
        "staff",
        "staff_payments",
        "cash_register",
    ]

    for table in insert_order:
        records = list(iterable_dataset[table])
        if not records:
            continue

        columns = table_columns[table]
        placeholders = ", ".join(["?"] * len(columns))
        statement = (
            f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
        )

        cursor.executemany(
            statement,
            [
                tuple(_normalize_value(record[column]) for column in columns)
                for record in records
            ],
        )


def _sanitize_payment_type(payment_type: PaymentTypeModel) -> dict:
    data = payment_type.to_dict()
    if isinstance(data.get("description"), tuple):
        data["description"] = data["description"][0]
    return data


def _normalize_value(value):  # type: ignore[no-untyped-def]
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (list, tuple)):
        return ", ".join(map(str, value))
    return value
