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
from models.settings_model import SettingsModel
from models.audit_log_model import AuditLogModel


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

    def _get_deletion_filter(self, deletion_status: str, table_alias: str = "") -> str:
        """
        Returns the SQL filter condition based on deletion_status.
        deletion_status: "active" (default), "deleted", "all"
        """
        prefix = f"{table_alias}." if table_alias else ""
        if deletion_status == "active":
            return f"{prefix}is_deleted = 0"
        elif deletion_status == "deleted":
            return f"{prefix}is_deleted = 1"
        return "1=1"  # No filter

    # ------------------------------------------------------------------
    # Users & Roles
    async def list_roles(self, deletion_status: str = "active") -> List[RoleModel]:
        filter_clause = self._get_deletion_filter(deletion_status)
        rows = await self._fetch_all(
            f"SELECT * FROM roles WHERE {filter_clause} ORDER BY id_role"
        )
        return [RoleModel(**dict(row)) for row in rows]

    async def list_users(self, deletion_status: str = "active") -> List[UserModel]:
        filter_clause = self._get_deletion_filter(deletion_status)
        rows = await self._fetch_all(
            f"SELECT * FROM users WHERE {filter_clause} ORDER BY username"
        )
        return [UserModel(**dict(row)) for row in rows]

    async def get_user(
        self, user_id: int, deletion_status: str = "active"
    ) -> Optional[UserModel]:
        filter_clause = self._get_deletion_filter(deletion_status)
        row = await self._fetch_one(
            f"SELECT * FROM users WHERE id_user = ? AND {filter_clause}", (user_id,)
        )
        return UserModel(**dict(row)) if row else None

    async def get_user_role(
        self, user_id: int, deletion_status: str = "active"
    ) -> RoleModel | None:
        # Note: We might want to check if the role itself is deleted too?
        # For now let's just check the user's deletion status if that's what's implied,
        # or maybe this method just retrieves the role for a user.
        # If the user is deleted, maybe we shouldn't find them.
        # But usually this is called after we have a user.
        # Let's assume we want to find the role even if the user is deleted, unless specified.
        # But the query joins users and roles.

        # Let's filter by user status.
        filter_clause = self._get_deletion_filter(deletion_status, "u")

        row = await self._fetch_one(
            f"""
            SELECT r.* FROM users u
            JOIN roles r ON u.role_id = r.id_role
            WHERE u.id_user = ? AND {filter_clause}
            """,
            (user_id,),
        )
        return RoleModel(**dict(row)) if row else None

    async def delete_role(self, role_id: int) -> bool:
        """Soft delete a role"""
        connection = await self._ensure_connection()
        try:
            await connection.execute(
                "UPDATE roles SET is_deleted = 1 WHERE id_role = ?",
                (role_id,),
            )
            await connection.commit()
            return True
        except Exception as e:
            print(f"Error deleting role: {e}")
            return False

    async def delete_user(self, user_id: int) -> bool:
        """Soft delete a user"""
        connection = await self._ensure_connection()
        try:
            await connection.execute(
                "UPDATE users SET is_deleted = 1 WHERE id_user = ?",
                (user_id,),
            )
            await connection.commit()
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False

    # ------------------------------------------------------------------
    # School years & classrooms
    async def list_school_years(
        self, deletion_status: str = "active"
    ) -> List[SchoolYearModel]:
        filter_clause = self._get_deletion_filter(deletion_status)
        rows = await self._fetch_all(
            f"SELECT * FROM school_years WHERE {filter_clause} ORDER BY start_date DESC"
        )
        return [self._row_to_school_year(row) for row in rows]

    async def get_active_school_year(self) -> Optional[SchoolYearModel]:
        # Active school year should probably not be deleted.
        row = await self._fetch_one(
            "SELECT * FROM school_years WHERE is_active = 1 AND is_deleted = 0 ORDER BY start_date DESC LIMIT 1"
        )
        return self._row_to_school_year(row) if row else None

    async def list_classrooms(
        self, deletion_status: str = "active"
    ) -> List[ClassroomModel]:
        filter_clause = self._get_deletion_filter(deletion_status)
        rows = await self._fetch_all(
            f"SELECT * FROM classrooms WHERE {filter_clause} ORDER BY level, name"
        )
        return [ClassroomModel(**dict(row)) for row in rows]

    async def delete_school_year(self, school_year_id: int) -> bool:
        """Soft delete a school year"""
        connection = await self._ensure_connection()
        try:
            await connection.execute(
                "UPDATE school_years SET is_deleted = 1 WHERE id_school_year = ?",
                (school_year_id,),
            )
            await connection.commit()
            return True
        except Exception as e:
            print(f"Error deleting school year: {e}")
            return False

    async def delete_classroom(self, classroom_id: int) -> bool:
        """Soft delete a classroom"""
        connection = await self._ensure_connection()
        try:
            await connection.execute(
                "UPDATE classrooms SET is_deleted = 1 WHERE id_classroom = ?",
                (classroom_id,),
            )
            await connection.commit()
            return True
        except Exception as e:
            print(f"Error deleting classroom: {e}")
            return False

    # ------------------------------------------------------------------
    # Students & enrollments
    async def list_students(
        self, deletion_status: str = "active"
    ) -> List[StudentModel]:
        filter_clause = self._get_deletion_filter(deletion_status)
        rows = await self._fetch_all(
            f"SELECT * FROM students WHERE {filter_clause} ORDER BY last_name, first_name"
        )
        return [StudentModel(**dict(row)) for row in rows]

    async def get_student(
        self, student_id: int, deletion_status: str = "active"
    ) -> Optional[StudentModel]:
        filter_clause = self._get_deletion_filter(deletion_status)
        row = await self._fetch_one(
            f"SELECT * FROM students WHERE id_student = ? AND {filter_clause}",
            (student_id,),
        )
        return StudentModel(**dict(row)) if row else None

    async def search_students(
        self, query: str, deletion_status: str = "active"
    ) -> List[StudentModel]:
        like = f"%{query.lower()}%"
        filter_clause = self._get_deletion_filter(deletion_status)
        rows = await self._fetch_all(
            f"""
            SELECT * FROM students
            WHERE (LOWER(first_name) LIKE ?
               OR LOWER(last_name) LIKE ?
               OR LOWER(surname) LIKE ?)
               AND {filter_clause}
            ORDER BY last_name, first_name
            """,
            (like, like, like),
        )
        return [StudentModel(**dict(row)) for row in rows]

    async def list_enrollments(
        self, deletion_status: str = "active"
    ) -> List[EnrollmentModel]:
        filter_clause = self._get_deletion_filter(deletion_status)
        rows = await self._fetch_all(
            f"SELECT * FROM enrollments WHERE {filter_clause} ORDER BY id_enrollment"
        )
        return [EnrollmentModel(**dict(row)) for row in rows]

    async def list_enrollments_by_student(
        self, student_id: int, deletion_status: str = "active"
    ) -> List[EnrollmentModel]:
        filter_clause = self._get_deletion_filter(deletion_status)
        rows = await self._fetch_all(
            f"SELECT * FROM enrollments WHERE student_id = ? AND {filter_clause} ORDER BY id_enrollment",
            (student_id,),
        )
        return [EnrollmentModel(**dict(row)) for row in rows]

    async def delete_enrollment(self, enrollment_id: int) -> bool:
        """Soft delete an enrollment"""
        connection = await self._ensure_connection()
        try:
            await connection.execute(
                "UPDATE enrollments SET is_deleted = 1 WHERE id_enrollment = ?",
                (enrollment_id,),
            )
            await connection.commit()
            return True
        except Exception as e:
            print(f"Error deleting enrollment: {e}")
            return False

    async def list_students_per_classroom(
        self, deletion_status: str = "active"
    ) -> Optional[Dict[str, List[StudentModel]]]:
        # We filter students and classrooms?
        # Let's filter students by default.
        filter_clause_s = self._get_deletion_filter(deletion_status, "s")
        filter_clause_c = self._get_deletion_filter(deletion_status, "c")

        rows = await self._fetch_all(
            f"""
            SELECT c.id_classroom, c.name, s.*
            FROM classrooms c
            JOIN enrollments e ON c.id_classroom = e.classroom_id
            JOIN students s ON e.student_id = s.id_student
            WHERE {filter_clause_s} AND {filter_clause_c}
            ORDER BY c.id_classroom, s.last_name, s.first_name
            """
        )
        if not rows:
            return None

        students_per_class: Dict[str, List[StudentModel]] = {}
        for row in rows:
            row_dict = dict(row)
            class_name = row_dict["name"]
            # We need to be careful not to pass extra fields to StudentModel if they are not in __init__
            # StudentModel now has is_deleted.
            # The query selects s.*, so it should have is_deleted.
            # But row_dict also has c.name and c.id_classroom.

            student_data = {
                k: v for k, v in row_dict.items() if k not in ("name", "id_classroom")
            }
            student = StudentModel(**student_data)
            students_per_class.setdefault(class_name, []).append(student)

        return students_per_class

    # ------------------------------------------------------------------
    # Payment types & payments
    async def list_payment_types(
        self, deletion_status: str = "active"
    ) -> List[PaymentTypeModel]:
        filter_clause = self._get_deletion_filter(deletion_status)
        rows = await self._fetch_all(
            f"SELECT * FROM payment_types WHERE {filter_clause} ORDER BY id_payment_type"
        )
        return [PaymentTypeModel(**dict(row)) for row in rows]

    async def list_payments(
        self, deletion_status: str = "active"
    ) -> List[PaymentModel]:
        filter_clause = self._get_deletion_filter(deletion_status)
        rows = await self._fetch_all(
            f"SELECT * FROM payments WHERE {filter_clause} ORDER BY payment_date DESC"
        )
        return [PaymentModel(**dict(row)) for row in rows]

    async def list_payments_by_student(
        self, student_id: int, deletion_status: str = "active"
    ) -> List[PaymentModel]:
        filter_clause = self._get_deletion_filter(deletion_status)
        rows = await self._fetch_all(
            f"SELECT * FROM payments WHERE student_id = ? AND {filter_clause} ORDER BY payment_date DESC",
            (student_id,),
        )
        return [PaymentModel(**dict(row)) for row in rows]

    async def delete_payment_type(self, payment_type_id: int) -> bool:
        """Soft delete a payment type"""
        connection = await self._ensure_connection()
        try:
            await connection.execute(
                "UPDATE payment_types SET is_deleted = 1 WHERE id_payment_type = ?",
                (payment_type_id,),
            )
            await connection.commit()
            return True
        except Exception as e:
            print(f"Error deleting payment type: {e}")
            return False

    async def delete_payment(self, payment_id: int) -> bool:
        """Soft delete a payment"""
        connection = await self._ensure_connection()
        try:
            await connection.execute(
                "UPDATE payments SET is_deleted = 1 WHERE id_payment = ?",
                (payment_id,),
            )
            await connection.commit()
            return True
        except Exception as e:
            print(f"Error deleting payment: {e}")
            return False

    # ------------------------------------------------------------------
    # Expenses & staff
    async def list_expenses(
        self, deletion_status: str = "active"
    ) -> List[ExpenseModel]:
        filter_clause = self._get_deletion_filter(deletion_status)
        rows = await self._fetch_all(
            f"SELECT * FROM expenses WHERE {filter_clause} ORDER BY expense_date DESC"
        )
        return [ExpenseModel(**dict(row)) for row in rows]

    async def list_staff(self, deletion_status: str = "active") -> List[StaffModel]:
        filter_clause = self._get_deletion_filter(deletion_status)
        rows = await self._fetch_all(
            f"SELECT * FROM staff WHERE {filter_clause} ORDER BY last_name, first_name"
        )
        return [StaffModel(**dict(row)) for row in rows]

    async def list_staff_payments(
        self, deletion_status: str = "active"
    ) -> List[StaffPaymentModel]:
        filter_clause = self._get_deletion_filter(deletion_status)
        rows = await self._fetch_all(
            f"SELECT * FROM staff_payments WHERE {filter_clause} ORDER BY payment_date DESC"
        )
        return [StaffPaymentModel(**dict(row)) for row in rows]

    async def list_staff_payments_by_staff(
        self, staff_id: int, deletion_status: str = "active"
    ) -> List[StaffPaymentModel]:
        filter_clause = self._get_deletion_filter(deletion_status)
        rows = await self._fetch_all(
            f"SELECT * FROM staff_payments WHERE staff_id = ? AND {filter_clause} ORDER BY payment_date DESC",
            (staff_id,),
        )
        return [StaffPaymentModel(**dict(row)) for row in rows]

    async def delete_expense(self, expense_id: int) -> bool:
        """Soft delete an expense"""
        connection = await self._ensure_connection()
        try:
            await connection.execute(
                "UPDATE expenses SET is_deleted = 1 WHERE id_expense = ?",
                (expense_id,),
            )
            await connection.commit()
            return True
        except Exception as e:
            print(f"Error deleting expense: {e}")
            return False

    async def delete_staff(self, staff_id: int) -> bool:
        """Soft delete a staff member"""
        connection = await self._ensure_connection()
        try:
            await connection.execute(
                "UPDATE staff SET is_deleted = 1 WHERE id_staff = ?",
                (staff_id,),
            )
            await connection.commit()
            return True
        except Exception as e:
            print(f"Error deleting staff: {e}")
            return False

    async def delete_staff_payment(self, staff_payment_id: int) -> bool:
        """Soft delete a staff payment"""
        connection = await self._ensure_connection()
        try:
            await connection.execute(
                "UPDATE staff_payments SET is_deleted = 1 WHERE id_staff_payment = ?",
                (staff_payment_id,),
            )
            await connection.commit()
            return True
        except Exception as e:
            print(f"Error deleting staff payment: {e}")
            return False

    # ------------------------------------------------------------------
    # Cash register & dashboard
    async def list_cash_register_entries(
        self, deletion_status: str = "active"
    ) -> List[CashRegisterModel]:
        filter_clause = self._get_deletion_filter(deletion_status)
        rows = await self._fetch_all(
            f"SELECT * FROM cash_register WHERE {filter_clause} ORDER BY date DESC"
        )
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

    async def delete_cash_register_entry(self, cash_id: int) -> bool:
        """Soft delete a cash register entry"""
        connection = await self._ensure_connection()
        try:
            await connection.execute(
                "UPDATE cash_register SET is_deleted = 1 WHERE id_cash = ?",
                (cash_id,),
            )
            await connection.commit()
            return True
        except Exception as e:
            print(f"Error deleting cash register entry: {e}")
            return False

    async def get_cash_register_statistics(
        self, school_year_id: int | None = None
    ) -> Dict[str, float]:
        """Get cash register statistics"""
        # Assuming we only want active entries for statistics
        if school_year_id:
            total_in = await self._scalar(
                "SELECT SUM(amount) FROM cash_register WHERE type = 'Entrée' AND school_year_id = ? AND is_deleted = 0",
                (school_year_id,),
            )
            total_out = await self._scalar(
                "SELECT SUM(amount) FROM cash_register WHERE type = 'Sortie' AND school_year_id = ? AND is_deleted = 0",
                (school_year_id,),
            )
        else:
            total_in = await self._scalar(
                "SELECT SUM(amount) FROM cash_register WHERE type = 'Entrée' AND is_deleted = 0"
            )
            total_out = await self._scalar(
                "SELECT SUM(amount) FROM cash_register WHERE type = 'Sortie' AND is_deleted = 0"
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
            "total_students": await self._scalar(
                "SELECT COUNT(*) FROM students WHERE is_deleted = 0"
            ),
            "total_payments": await self._scalar(
                "SELECT COUNT(*) FROM payments WHERE is_deleted = 0"
            ),
            "total_expenses": await self._scalar(
                "SELECT COUNT(*) FROM expenses WHERE is_deleted = 0"
            ),
        }
        summary["amount_payments"] = (
            await self._scalar("SELECT SUM(amount) FROM payments WHERE is_deleted = 0")
            or 0.0
        )
        summary["amount_expenses"] = (
            await self._scalar("SELECT SUM(amount) FROM expenses WHERE is_deleted = 0")
            or 0.0
        )
        summary["cash_balance"] = (
            summary["amount_payments"] - summary["amount_expenses"]
        )

        active_school_year = await self.get_active_school_year()
        summary["active_school_year"] = (
            active_school_year.name if active_school_year else "N/A"
        )

        # Nombre d'eleves par classe : {class : student}
        students_per_classroom = await self.list_students_per_classroom(
            deletion_status="active"
        )
        if students_per_classroom:
            students_per_classroom = {
                c: len(s) for c, s in students_per_classroom.items()
            }
        else:
            students_per_classroom = {}

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

    async def create_student(self, student: StudentModel) -> bool:
        """Create a new student"""
        connection = await self._ensure_connection()
        try:
            await connection.execute(
                """
                INSERT INTO students (first_name, last_name, surname, gender, 
                                     date_of_birth, address, parent_contact)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    student.first_name,
                    student.last_name,
                    student.surname,
                    student.gender,
                    student.date_of_birth,
                    student.address,
                    student.parent_contact,
                ),
            )
            await connection.commit()
            return True
        except Exception as e:
            print(f"Error creating student: {e}")
            return False

    async def import_students(
        self, students_list: List[StudentModel], classroom_id: int
    ) -> tuple[bool, int]:
        """Import multiple students and enroll them in a classroom"""
        connection = await self._ensure_connection()
        imported_count = 0

        try:
            # Get active school year
            active_year = await self.get_active_school_year()
            if not active_year:
                return False, 0

            for student in students_list:
                try:
                    # Insert student
                    cursor = await connection.execute(
                        """
                        INSERT INTO students (first_name, last_name, surname, gender, 
                                             date_of_birth, address, parent_contact)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            student.first_name,
                            student.last_name,
                            student.surname,
                            student.gender,
                            student.date_of_birth,
                            student.address,
                            student.parent_contact,
                        ),
                    )
                    student_id = cursor.lastrowid

                    # Create enrollment
                    await connection.execute(
                        """
                        INSERT INTO enrollments (student_id, classroom_id, school_year_id)
                        VALUES (?, ?, ?)
                        """,
                        (student_id, classroom_id, active_year.id_school_year),
                    )

                    imported_count += 1
                except Exception as e:
                    print(
                        f"Error importing student {student.first_name} {student.last_name}: {e}"
                    )
                    continue

            await connection.commit()
            return True, imported_count
        except Exception as e:
            print(f"Error during import: {e}")
            await connection.rollback()
            return False, imported_count

    async def update_student(self, student: StudentModel) -> bool:
        """Update an existing student"""
        connection = await self._ensure_connection()
        try:
            await connection.execute(
                """
                UPDATE students 
                SET first_name = ?, last_name = ?, surname = ?, gender = ?,
                    date_of_birth = ?, address = ?, parent_contact = ?
                WHERE id_student = ?
                """,
                (
                    student.first_name,
                    student.last_name,
                    student.surname,
                    student.gender,
                    student.date_of_birth,
                    student.address,
                    student.parent_contact,
                    student.id_student,
                ),
            )
            await connection.commit()
            return True
        except Exception as e:
            print(f"Error updating student: {e}")
            return False

    async def delete_student(self, student_id: int) -> bool:
        """Soft delete a student"""
        connection = await self._ensure_connection()
        try:
            await connection.execute(
                "UPDATE students SET is_deleted = 1 WHERE id_student = ?",
                (student_id,),
            )
            await connection.commit()
            return True
        except Exception as e:
            print(f"Error deleting student: {e}")
            return False

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

    # ------------------------------------------------------------------
    # Settings & Audit Logs
    async def get_setting(self, key: str) -> Optional[str]:
        row = await self._fetch_one("SELECT value FROM settings WHERE key = ?", (key,))
        return row["value"] if row else None

    async def set_setting(self, key: str, value: str, description: str = "") -> bool:
        connection = await self._ensure_connection()
        try:
            await connection.execute(
                """
                INSERT INTO settings (key, value, description) VALUES (?, ?, ?)
                ON CONFLICT(key) DO UPDATE SET value = excluded.value, description = excluded.description
                """,
                (key, value, description),
            )
            await connection.commit()
            return True
        except Exception as e:
            print(f"Error setting setting {key}: {e}")
            return False

    async def list_settings(self) -> List[SettingsModel]:
        rows = await self._fetch_all("SELECT * FROM settings ORDER BY key")
        return [SettingsModel(**dict(row)) for row in rows]

    async def log_action(
        self,
        user_id: int,
        action: str,
        table_name: str,
        record_id: int,
        details: str = "",
    ) -> bool:
        connection = await self._ensure_connection()
        try:
            from datetime import datetime

            timestamp = datetime.now().isoformat()
            await connection.execute(
                """
                INSERT INTO audit_logs (user_id, action, table_name, record_id, timestamp, details)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (user_id, action, table_name, record_id, timestamp, details),
            )
            await connection.commit()
            return True
        except Exception as e:
            print(f"Error logging action: {e}")
            return False

    async def list_audit_logs(self, limit: int = 100) -> List[AuditLogModel]:
        rows = await self._fetch_all(
            f"SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT {limit}"
        )
        return [AuditLogModel(**dict(row)) for row in rows]
