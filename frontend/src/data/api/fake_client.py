"""Client API fictif alimenté par SQLite pour les tests."""

from __future__ import annotations

import asyncio
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import aiosqlite
from aiosqlite import Connection, Row

from data.fake.fake_data import FAKE_DB_PATH, initialize_fake_database
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


class FakeApiClient:
    """Client simulant des endpoints REST pour les besoins de développement."""

    def __init__(
        self,
        db_path: Path | str | None = None,
        seed: int | None = None,
        auto_seed: bool = True,
    ) -> None:
        self._db_path = Path(db_path) if db_path else FAKE_DB_PATH
        if auto_seed or not self._db_path.exists():
            initialize_fake_database(self._db_path, seed=seed)

        self._connection: Optional[Connection] = None
        self._connection_lock = asyncio.Lock()

    # ------------------------------------------------------------------
    # Lifecycle helpers
    async def __aenter__(self) -> "FakeApiClient":
        await self._ensure_connection()
        return self

    async def __aexit__(self, exc_type, exc, traceback) -> None:  # type: ignore[override]
        await self.close()

    async def close(self) -> None:
        """Ferme la connexion SQLite asynchrone."""

        if self._connection is not None:
            await self._connection.close()
            self._connection = None

    async def reset(self, seed: int | None = None) -> None:
        """Re-génère la base de données avec un nouveau jeu de données."""
        await self.close()
        initialize_fake_database(self._db_path, seed=seed)

    async def _ensure_connection(self) -> Connection:
        """Crée une connexion aiosqlite si nécessaire et la réutilise."""

        if self._connection is None:
            async with self._connection_lock:
                if self._connection is None:
                    connection = await aiosqlite.connect(self._db_path)
                    connection.row_factory = Row
                    self._connection = connection
        return self._connection

    # ------------------------------------------------------------------
    # Users & Roles
    async def list_roles(self) -> List[RoleModel]:
        rows = await self._fetch_all("SELECT * FROM roles ORDER BY id_role")
        return [RoleModel(**dict(row)) for row in rows]

    async def list_users(self) -> List[UserModel]:
        rows = await self._fetch_all("SELECT * FROM users ORDER BY username")
        return [UserModel(**dict(row)) for row in rows]

    async def get_user(self, user_id: int) -> Optional[UserModel]:
        row = await self._fetch_one("SELECT * FROM users WHERE id_user = ?", (user_id,))
        return UserModel(**dict(row)) if row else None

    async def get_user_role(self, user_id: int) -> RoleModel | None:
        row = await self._fetch_one(
            """
            SELECT r.* FROM users u
            JOIN roles r ON u.role_id = r.id_role
            WHERE u.id_user = ?
            """,
            (user_id,),
        )
        return RoleModel(**dict(row)) if row else None

    # ------------------------------------------------------------------
    # School years & classrooms
    async def list_school_years(self) -> List[SchoolYearModel]:
        rows = await self._fetch_all(
            "SELECT * FROM school_years ORDER BY start_date DESC"
        )
        return [self._row_to_school_year(row) for row in rows]

    async def get_active_school_year(self) -> Optional[SchoolYearModel]:
        row = await self._fetch_one(
            "SELECT * FROM school_years WHERE is_active = 1 ORDER BY start_date DESC LIMIT 1"
        )
        return self._row_to_school_year(row) if row else None

    async def list_classrooms(self) -> List[ClassroomModel]:
        rows = await self._fetch_all("SELECT * FROM classrooms ORDER BY level, name")
        return [ClassroomModel(**dict(row)) for row in rows]

    # ------------------------------------------------------------------
    # Students & enrollments
    async def list_students(self) -> List[StudentModel]:
        rows = await self._fetch_all(
            "SELECT * FROM students ORDER BY last_name, first_name"
        )
        return [StudentModel(**dict(row)) for row in rows]

    async def get_student(self, student_id: int) -> Optional[StudentModel]:
        row = await self._fetch_one(
            "SELECT * FROM students WHERE id_student = ?", (student_id,)
        )
        return StudentModel(**dict(row)) if row else None

    async def search_students(self, query: str) -> List[StudentModel]:
        like = f"%{query.lower()}%"
        rows = await self._fetch_all(
            """
            SELECT * FROM students
            WHERE LOWER(first_name) LIKE ?
               OR LOWER(last_name) LIKE ?
               OR LOWER(surname) LIKE ?
            ORDER BY last_name, first_name
            """,
            (like, like, like),
        )
        return [StudentModel(**dict(row)) for row in rows]

    async def list_enrollments(self) -> List[EnrollmentModel]:
        rows = await self._fetch_all("SELECT * FROM enrollments ORDER BY id_enrollment")
        return [EnrollmentModel(**dict(row)) for row in rows]

    async def list_enrollments_by_student(
        self, student_id: int
    ) -> List[EnrollmentModel]:
        rows = await self._fetch_all(
            "SELECT * FROM enrollments WHERE student_id = ? ORDER BY id_enrollment",
            (student_id,),
        )
        return [EnrollmentModel(**dict(row)) for row in rows]

    async def list_students_per_classroom(
        self,
    ) -> Optional[Dict[str, List[StudentModel]]]:
        rows = await self._fetch_all(
            """
            SELECT c.id_classroom, c.name, s.*
            FROM classrooms c
            JOIN enrollments e ON c.id_classroom = e.classroom_id
            JOIN students s ON e.student_id = s.id_student
            ORDER BY c.id_classroom, s.last_name, s.first_name
            """
        )
        if not rows:
            return None

        students_per_class: Dict[str, List[StudentModel]] = {}
        for row in rows:
            row_dict = dict(row)
            class_name = row_dict["name"]
            student = StudentModel(
                **{
                    k: v
                    for k, v in row_dict.items()
                    if k not in ("name", "id_classroom")
                }
            )
            students_per_class.setdefault(class_name, []).append(student)

        return students_per_class

    # ------------------------------------------------------------------
    # Payment types & payments
    async def list_payment_types(self) -> List[PaymentTypeModel]:
        rows = await self._fetch_all(
            "SELECT * FROM payment_types ORDER BY id_payment_type"
        )
        return [PaymentTypeModel(**dict(row)) for row in rows]

    async def list_payments(self) -> List[PaymentModel]:
        rows = await self._fetch_all(
            "SELECT * FROM payments ORDER BY payment_date DESC"
        )
        return [PaymentModel(**dict(row)) for row in rows]

    async def list_payments_by_student(self, student_id: int) -> List[PaymentModel]:
        rows = await self._fetch_all(
            "SELECT * FROM payments WHERE student_id = ? ORDER BY payment_date DESC",
            (student_id,),
        )
        return [PaymentModel(**dict(row)) for row in rows]

    # ------------------------------------------------------------------
    # Expenses & staff
    async def list_expenses(self) -> List[ExpenseModel]:
        rows = await self._fetch_all(
            "SELECT * FROM expenses ORDER BY expense_date DESC"
        )
        return [ExpenseModel(**dict(row)) for row in rows]

    async def list_staff(self) -> List[StaffModel]:
        rows = await self._fetch_all(
            "SELECT * FROM staff ORDER BY last_name, first_name"
        )
        return [StaffModel(**dict(row)) for row in rows]

    async def list_staff_payments(self) -> List[StaffPaymentModel]:
        rows = await self._fetch_all(
            "SELECT * FROM staff_payments ORDER BY payment_date DESC"
        )
        return [StaffPaymentModel(**dict(row)) for row in rows]

    async def list_staff_payments_by_staff(
        self, staff_id: int
    ) -> List[StaffPaymentModel]:
        rows = await self._fetch_all(
            "SELECT * FROM staff_payments WHERE staff_id = ? ORDER BY payment_date DESC",
            (staff_id,),
        )
        return [StaffPaymentModel(**dict(row)) for row in rows]

    # ------------------------------------------------------------------
    # Cash register & dashboard
    async def list_cash_register_entries(self) -> List[CashRegisterModel]:
        rows = await self._fetch_all("SELECT * FROM cash_register ORDER BY date DESC")
        return [CashRegisterModel(**dict(row)) for row in rows]

    async def create_cash_register_entry(
        self,
        school_year_id: int,
        date: str,
        type: str,
        description: str,
        amount: float,
        user_id: int,
    ) -> CashRegisterModel:
        """Create a new cash register entry"""
        connection = await self._ensure_connection()
        async with connection.execute(
            """
            INSERT INTO cash_register (school_year_id, date, type, description, amount, user_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (school_year_id, date, type, description, amount, user_id),
        ) as cursor:
            await connection.commit()
            new_id = cursor.lastrowid
        return CashRegisterModel(
            id_cash=new_id,
            school_year_id=school_year_id,
            date=date,
            type=type,
            description=description,
            amount=amount,
            user_id=user_id,
        )

    async def get_cash_register_statistics(
        self, school_year_id: int | None = None
    ) -> Dict[str, float]:
        """Get cash register statistics"""
        if school_year_id:
            total_in = await self._scalar(
                "SELECT SUM(amount) FROM cash_register WHERE type = 'Entrée' AND school_year_id = ?",
                (school_year_id,),
            )
            total_out = await self._scalar(
                "SELECT SUM(amount) FROM cash_register WHERE type = 'Sortie' AND school_year_id = ?",
                (school_year_id,),
            )
        else:
            total_in = await self._scalar(
                "SELECT SUM(amount) FROM cash_register WHERE type = 'Entrée'"
            )
            total_out = await self._scalar(
                "SELECT SUM(amount) FROM cash_register WHERE type = 'Sortie'"
            )

        balance = (total_in or 0.0) - (total_out or 0.0)

        return {
            "total_in": total_in or 0.0,
            "total_out": total_out or 0.0,
            "balance": balance,
        }

    async def create_expense(
        self,
        school_year_id: int,
        expense_date: str,
        description: str,
        amount: float,
        user_id: int,
    ) -> ExpenseModel:
        """Create a new expense and register it in cash register"""
        connection = await self._ensure_connection()

        # Create expense
        async with connection.execute(
            """
            INSERT INTO expenses (school_year_id, expense_date, description, amount, user_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            (school_year_id, expense_date, description, amount, user_id),
        ) as cursor:
            await connection.commit()
            expense_id = cursor.lastrowid

        # Create cash register entry
        await connection.execute(
            """
            INSERT INTO cash_register (school_year_id, date, type, description, amount, user_id)
            VALUES (?, ?, 'Sortie', ?, ?, ?)
            """,
            (school_year_id, expense_date, f"Dépense: {description}", amount, user_id),
        )
        await connection.commit()

        return ExpenseModel(
            id_expense=expense_id,
            school_year_id=school_year_id,
            expense_date=expense_date,
            description=description,
            amount=amount,
            user_id=user_id,
        )

    async def create_staff_payment(
        self,
        staff_id: int,
        school_year_id: int,
        amount: float,
        payment_date: str,
        user_id: int,
    ) -> StaffPaymentModel:
        """Create a new staff payment and register it in cash register"""
        connection = await self._ensure_connection()

        # Get staff name
        staff_row = await self._fetch_one(
            "SELECT first_name, last_name FROM staff WHERE id_staff = ?", (staff_id,)
        )
        staff_name = (
            f"{staff_row['first_name']} {staff_row['last_name']}"
            if staff_row
            else "Unknown"
        )

        # Create staff payment
        async with connection.execute(
            """
            INSERT INTO staff_payments (staff_id, school_year_id, amount, payment_date, user_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            (staff_id, school_year_id, amount, payment_date, user_id),
        ) as cursor:
            await connection.commit()
            payment_id = cursor.lastrowid

        # Create cash register entry
        await connection.execute(
            """
            INSERT INTO cash_register (school_year_id, date, type, description, amount, user_id)
            VALUES (?, ?, 'Sortie', ?, ?, ?)
            """,
            (
                school_year_id,
                payment_date,
                f"Paie du personnel: {staff_name}",
                amount,
                user_id,
            ),
        )
        await connection.commit()

        return StaffPaymentModel(
            id_staff_payment=payment_id,
            staff_id=staff_id,
            school_year_id=school_year_id,
            amount=amount,
            payment_date=payment_date,
            user_id=user_id,
        )

    async def get_dashboard_summary(self) -> Dict[str, float]:
        summary: Dict[str, float] = {
            "total_students": await self._scalar("SELECT COUNT(*) FROM students"),
            "total_payments": await self._scalar("SELECT COUNT(*) FROM payments"),
            "total_expenses": await self._scalar("SELECT COUNT(*) FROM expenses"),
        }
        summary["amount_payments"] = (
            await self._scalar("SELECT SUM(amount) FROM payments") or 0.0
        )
        summary["amount_expenses"] = (
            await self._scalar("SELECT SUM(amount) FROM expenses") or 0.0
        )
        summary["cash_balance"] = (
            summary["amount_payments"] - summary["amount_expenses"]
        )

        active_school_year = await self.get_active_school_year()
        summary["active_school_year"] = active_school_year.name

        # Nombre d'eleves par classe : {class : student}
        students_per_classroom = await self.list_students_per_classroom()
        students_per_classroom = {c: len(s) for c, s in students_per_classroom.items()}
        summary["students_per_classroom"] = students_per_classroom

        return summary

    async def get_student_financial_statement(
        self, student_id: int
    ) -> Dict[str, float]:
        payments = await self.list_payments_by_student(student_id)
        totals = defaultdict(float)
        for payment in payments:
            totals["total_paid"] += payment.amount
        totals["payments_count"] = float(len(payments))
        return totals

    # ------------------------------------------------------------------
    # Low level helpers
    def _row_to_school_year(self, row: Row) -> SchoolYearModel:
        data = dict(row)
        data["is_active"] = bool(data["is_active"])
        return SchoolYearModel(**data)

    async def _fetch_all(
        self, query: str, parameters: Iterable | None = None
    ) -> List[Row]:
        connection = await self._ensure_connection()
        async with connection.execute(query, tuple(parameters or ())) as cursor:
            rows = await cursor.fetchall()
        return list(rows)

    async def _fetch_one(
        self, query: str, parameters: Iterable | None = None
    ) -> Optional[Row]:
        connection = await self._ensure_connection()
        async with connection.execute(query, tuple(parameters or ())) as cursor:
            return await cursor.fetchone()

    async def _scalar(self, query: str, parameters: Iterable | None = None) -> float:
        connection = await self._ensure_connection()
        async with connection.execute(query, tuple(parameters or ())) as cursor:
            result = await cursor.fetchone()
        return float(result[0]) if result and result[0] is not None else 0.0


__all__ = ["FakeApiClient"]
