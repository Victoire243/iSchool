"""
Reports Services Module
Handles all business logic and API calls for the reports screen
"""

import asyncio
from datetime import datetime
from typing import Optional, List, Dict, Any
from core import AppState
from models import (
    StudentModel,
    StaffModel,
    PaymentModel,
    StaffPaymentModel,
    ClassroomModel,
    EnrollmentModel,
    CashRegisterModel,
    ExpenseModel,
    UserModel,
)


class ReportsServices:
    """Service class for reports operations"""

    def __init__(self, app_state: AppState):
        self.app_state = app_state

    # ========================================================================
    # DATA LOADING METHODS
    # ========================================================================

    async def load_students_list(self):
        """Load all students"""
        try:
            students = await self.app_state.api_client.list_students()
            return (True, students)
        except Exception as e:
            print(f"Error loading students list: {e}")
            return (False, [])

    async def load_students_by_classroom(self, classroom_id: int):
        """Load students by classroom"""
        try:
            students = await self.app_state.api_client.list_students_per_classroom(
                classroom_id
            )
            return (True, students)
        except Exception as e:
            print(f"Error loading students by classroom: {e}")
            return (False, [])

    async def load_staff_list(self):
        """Load all staff members"""
        try:
            staff = await self.app_state.api_client.list_staff()
            return (True, staff)
        except Exception as e:
            print(f"Error loading staff list: {e}")
            return (False, [])

    async def load_classrooms_list(self):
        """Load all classrooms"""
        try:
            classrooms = await self.app_state.api_client.list_classrooms()
            return (True, classrooms)
        except Exception as e:
            print(f"Error loading classrooms list: {e}")
            return (False, [])

    async def load_payments_list(self):
        """Load all payments"""
        try:
            payments = await self.app_state.api_client.list_payments()
            return (True, payments)
        except Exception as e:
            print(f"Error loading payments list: {e}")
            return (False, [])

    async def load_staff_payments_list(self):
        """Load all staff payments"""
        try:
            payments = await self.app_state.api_client.list_staff_payments()
            return (True, payments)
        except Exception as e:
            print(f"Error loading staff payments list: {e}")
            return (False, [])

    async def load_cash_register_entries(self):
        """Load all cash register entries"""
        try:
            entries = await self.app_state.api_client.list_cash_register_entries()
            return (True, entries)
        except Exception as e:
            print(f"Error loading cash register entries: {e}")
            return (False, [])

    async def load_expenses_list(self):
        """Load all expenses"""
        try:
            expenses = await self.app_state.api_client.list_expenses()
            return (True, expenses)
        except Exception as e:
            print(f"Error loading expenses list: {e}")
            return (False, [])

    async def load_users_list(self):
        """Load all users"""
        try:
            users = await self.app_state.api_client.list_users()
            return (True, users)
        except Exception as e:
            print(f"Error loading users list: {e}")
            return (False, [])

    async def load_enrollments_list(self):
        """Load all enrollments"""
        try:
            enrollments = await self.app_state.api_client.list_enrollments()
            return (True, enrollments)
        except Exception as e:
            print(f"Error loading enrollments list: {e}")
            return (False, [])

    # ========================================================================
    # REPORT GENERATION METHODS
    # ========================================================================

    async def generate_students_report(
        self,
        classroom_id: Optional[int] = None,
        format: str = "all",
    ) -> tuple[bool, List[Dict[str, Any]]]:
        """Generate students report"""
        try:
            if classroom_id:
                success, students = await self.load_students_by_classroom(classroom_id)
            else:
                success, students = await self.load_students_list()

            if not success:
                return (False, [])

            # Get enrollments to include classroom info
            _, enrollments = await self.load_enrollments_list()
            _, classrooms = await self.load_classrooms_list()

            # Create enrollment map
            enrollment_map = {}
            for enrollment in enrollments:
                enrollment_map[enrollment.id_student] = enrollment.id_classroom

            # Create classroom map
            classroom_map = {c.id_classroom: c.name for c in classrooms}

            report_data = []
            for student in students:
                classroom_name = "N/A"
                if student.id_student in enrollment_map:
                    classroom_id_mapped = enrollment_map[student.id_student]
                    classroom_name = classroom_map.get(classroom_id_mapped, "N/A")

                report_data.append(
                    {
                        "id": student.id_student,
                        "first_name": student.first_name,
                        "last_name": student.last_name,
                        "gender": student.gender,
                        "date_of_birth": student.date_of_birth,
                        "contact": student.contact or "N/A",
                        "address": student.address or "N/A",
                        "classroom": classroom_name,
                    }
                )

            return (True, report_data)
        except Exception as e:
            print(f"Error generating students report: {e}")
            return (False, [])

    async def generate_staff_payments_report(
        self,
        staff_id: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> tuple[bool, List[Dict[str, Any]]]:
        """Generate staff payments report"""
        try:
            if staff_id:
                payments = await self.app_state.api_client.list_staff_payments_by_staff(
                    staff_id
                )
                success = True
            else:
                success, payments = await self.load_staff_payments_list()

            if not success:
                return (False, [])

            # Load staff info
            _, staff_list = await self.load_staff_list()
            staff_map = {s.id_staff: s for s in staff_list}

            report_data = []
            for payment in payments:
                # Filter by date if provided
                if start_date and payment.payment_date < start_date:
                    continue
                if end_date and payment.payment_date > end_date:
                    continue

                staff = staff_map.get(payment.id_staff)
                staff_name = (
                    f"{staff.first_name} {staff.last_name}" if staff else "Unknown"
                )

                report_data.append(
                    {
                        "id": payment.id_staff_payment,
                        "staff_name": staff_name,
                        "payment_date": payment.payment_date,
                        "amount": payment.amount,
                        "payment_type": payment.payment_type or "Salary",
                        "description": payment.description or "N/A",
                    }
                )

            return (True, report_data)
        except Exception as e:
            print(f"Error generating staff payments report: {e}")
            return (False, [])

    async def generate_financial_report_by_classroom(
        self,
        classroom_id: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> tuple[bool, Dict[str, Any]]:
        """Generate financial report by classroom"""
        try:
            success, payments = await self.load_payments_list()
            if not success:
                return (False, {})

            _, students = await self.load_students_list()
            _, enrollments = await self.load_enrollments_list()
            _, classrooms = await self.load_classrooms_list()

            # Create maps
            enrollment_map = {}
            for enrollment in enrollments:
                enrollment_map[enrollment.id_student] = enrollment.id_classroom

            classroom_map = {c.id_classroom: c.name for c in classrooms}
            student_map = {s.id_student: s for s in students}

            # Aggregate by classroom
            classroom_totals = {}
            for payment in payments:
                # Filter by date if provided
                if start_date and payment.payment_date < start_date:
                    continue
                if end_date and payment.payment_date > end_date:
                    continue

                student_id = payment.id_student
                if student_id not in enrollment_map:
                    continue

                class_id = enrollment_map[student_id]

                # Filter by specific classroom if provided
                if classroom_id and class_id != classroom_id:
                    continue

                class_name = classroom_map.get(class_id, f"Classroom {class_id}")

                if class_name not in classroom_totals:
                    classroom_totals[class_name] = {
                        "total_amount": 0.0,
                        "payment_count": 0,
                        "students": set(),
                    }

                classroom_totals[class_name]["total_amount"] += payment.amount
                classroom_totals[class_name]["payment_count"] += 1
                classroom_totals[class_name]["students"].add(student_id)

            # Convert to list
            report_data = []
            for class_name, data in classroom_totals.items():
                report_data.append(
                    {
                        "classroom": class_name,
                        "total_amount": data["total_amount"],
                        "payment_count": data["payment_count"],
                        "student_count": len(data["students"]),
                    }
                )

            return (
                True,
                {
                    "classrooms": report_data,
                    "total": sum(d["total_amount"] for d in report_data),
                },
            )
        except Exception as e:
            print(f"Error generating financial report by classroom: {e}")
            return (False, {})

    async def generate_financial_report_by_student(
        self,
        student_id: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> tuple[bool, List[Dict[str, Any]]]:
        """Generate financial report by student"""
        try:
            if student_id:
                payments = await self.app_state.api_client.list_payments_by_student(
                    student_id
                )
                success = True
            else:
                success, payments = await self.load_payments_list()

            if not success:
                return (False, [])

            _, students = await self.load_students_list()
            student_map = {s.id_student: s for s in students}

            # Aggregate by student
            student_totals = {}
            for payment in payments:
                # Filter by date if provided
                if start_date and payment.payment_date < start_date:
                    continue
                if end_date and payment.payment_date > end_date:
                    continue

                student_id_key = payment.id_student
                if student_id_key not in student_totals:
                    student = student_map.get(student_id_key)
                    student_name = (
                        f"{student.first_name} {student.last_name}"
                        if student
                        else "Unknown"
                    )
                    student_totals[student_id_key] = {
                        "student_name": student_name,
                        "total_amount": 0.0,
                        "payment_count": 0,
                    }

                student_totals[student_id_key]["total_amount"] += payment.amount
                student_totals[student_id_key]["payment_count"] += 1

            report_data = [
                {
                    "student_id": sid,
                    "student_name": data["student_name"],
                    "total_amount": data["total_amount"],
                    "payment_count": data["payment_count"],
                }
                for sid, data in student_totals.items()
            ]

            return (True, report_data)
        except Exception as e:
            print(f"Error generating financial report by student: {e}")
            return (False, [])

    async def generate_school_financial_report(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> tuple[bool, Dict[str, Any]]:
        """Generate overall school financial report"""
        try:
            success_payments, payments = await self.load_payments_list()
            success_staff_payments, staff_payments = (
                await self.load_staff_payments_list()
            )
            success_expenses, expenses = await self.load_expenses_list()

            if not (success_payments and success_staff_payments and success_expenses):
                return (False, {})

            total_income = 0.0
            total_expenses = 0.0
            payment_count = 0
            staff_payment_count = 0
            expense_count = 0

            # Calculate income from student payments
            for payment in payments:
                if start_date and payment.payment_date < start_date:
                    continue
                if end_date and payment.payment_date > end_date:
                    continue
                total_income += payment.amount
                payment_count += 1

            # Calculate expenses from staff payments
            for payment in staff_payments:
                if start_date and payment.payment_date < start_date:
                    continue
                if end_date and payment.payment_date > end_date:
                    continue
                total_expenses += payment.amount
                staff_payment_count += 1

            # Calculate expenses from general expenses
            for expense in expenses:
                if start_date and expense.date < start_date:
                    continue
                if end_date and expense.date > end_date:
                    continue
                total_expenses += expense.amount
                expense_count += 1

            report_data = {
                "total_income": total_income,
                "total_expenses": total_expenses,
                "net_balance": total_income - total_expenses,
                "payment_count": payment_count,
                "staff_payment_count": staff_payment_count,
                "expense_count": expense_count,
            }

            return (True, report_data)
        except Exception as e:
            print(f"Error generating school financial report: {e}")
            return (False, {})

    async def generate_cash_register_report(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> tuple[bool, List[Dict[str, Any]]]:
        """Generate cash register report"""
        try:
            success, entries = await self.load_cash_register_entries()
            if not success:
                return (False, [])

            report_data = []
            for entry in entries:
                # Filter by date if provided
                if start_date and entry.date < start_date:
                    continue
                if end_date and entry.date > end_date:
                    continue

                report_data.append(
                    {
                        "id": entry.id_cash_register,
                        "date": entry.date,
                        "type": entry.type,
                        "description": entry.description or "N/A",
                        "amount": entry.amount,
                    }
                )

            return (True, report_data)
        except Exception as e:
            print(f"Error generating cash register report: {e}")
            return (False, [])

    async def generate_users_report(self) -> tuple[bool, List[Dict[str, Any]]]:
        """Generate users report"""
        try:
            success, users = await self.load_users_list()
            if not success:
                return (False, [])

            report_data = []
            for user in users:
                report_data.append(
                    {
                        "id": user.id_user,
                        "username": user.username,
                        "role_id": user.role_id,
                        "is_active": "Yes" if user.is_active else "No",
                    }
                )

            return (True, report_data)
        except Exception as e:
            print(f"Error generating users report: {e}")
            return (False, [])
