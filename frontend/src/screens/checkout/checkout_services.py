"""
Checkout Services Module
Handles all business logic and API calls for the checkout screen
"""

import asyncio
from datetime import datetime
from core import AppState
from models import (
    CashRegisterModel,
    ExpenseModel,
    StaffPaymentModel,
    StaffModel,
    PaymentModel,
)


class CheckoutServices:
    """Service class for checkout operations"""

    def __init__(self, app_state: AppState):
        self.app_state = app_state

    async def load_cash_register_entries(self):
        """Load all cash register entries"""
        try:
            entries = await self.app_state.api_client.list_cash_register_entries()
            return (True, entries)
        except Exception as e:
            print(f"Error loading cash register entries: {e}")
            return (False, [])

    async def load_expenses(self):
        """Load all expenses"""
        try:
            expenses = await self.app_state.api_client.list_expenses()
            return (True, expenses)
        except Exception as e:
            print(f"Error loading expenses: {e}")
            return (False, [])

    async def load_staff_payments(self):
        """Load all staff payments"""
        try:
            payments = await self.app_state.api_client.list_staff_payments()
            return (True, payments)
        except Exception as e:
            print(f"Error loading staff payments: {e}")
            return (False, [])

    async def load_staff_list(self):
        """Load all staff members"""
        try:
            staff = await self.app_state.api_client.list_staff()
            return (True, staff)
        except Exception as e:
            print(f"Error loading staff list: {e}")
            return (False, [])

    async def load_student_payments(self):
        """Load all student payments"""
        try:
            payments = await self.app_state.api_client.list_payments()
            return (True, payments)
        except Exception as e:
            print(f"Error loading student payments: {e}")
            return (False, [])

    async def get_cash_statistics(self, school_year_id: int | None = None):
        """Get cash register statistics"""
        try:
            stats = await self.app_state.api_client.get_cash_register_statistics(
                school_year_id
            )
            return (True, stats)
        except Exception as e:
            print(f"Error loading cash statistics: {e}")
            return (False, {"total_in": 0.0, "total_out": 0.0, "balance": 0.0})

    async def create_quick_entry(
        self, description: str, amount: float, entry_type: str
    ):
        """Create a quick cash register entry"""
        try:
            school_year = await self.app_state.api_client.get_active_school_year()
            if not school_year:
                return (False, "No active school year found")

            entry = await self.app_state.api_client.create_cash_register_entry(
                school_year_id=school_year.id_school_year,
                date=datetime.now().strftime("%d-%m-%Y"),
                type=entry_type,
                description=description,
                amount=amount,
                user_id=self.app_state.current_user.id_user,
            )
            return (True, entry)
        except Exception as e:
            print(f"Error creating quick entry: {e}")
            return (False, str(e))

    async def create_quick_expense(self, description: str, amount: float):
        """Create a quick expense"""
        try:
            school_year = await self.app_state.api_client.get_active_school_year()
            if not school_year:
                return (False, "No active school year found")

            expense = await self.app_state.api_client.create_expense(
                school_year_id=school_year.id_school_year,
                expense_date=datetime.now().strftime("%d-%m-%Y"),
                description=description,
                amount=amount,
                user_id=self.app_state.current_user.id_user,
            )
            return (True, expense)
        except Exception as e:
            print(f"Error creating quick expense: {e}")
            return (False, str(e))

    async def create_staff_payment(self, staff_id: int, amount: float):
        """Create a staff payment"""
        try:
            school_year = await self.app_state.api_client.get_active_school_year()
            if not school_year:
                return (False, "No active school year found")

            payment = await self.app_state.api_client.create_staff_payment(
                staff_id=staff_id,
                school_year_id=school_year.id_school_year,
                amount=amount,
                payment_date=datetime.now().strftime("%d-%m-%Y"),
                user_id=self.app_state.current_user.id_user,
            )
            return (True, payment)
        except Exception as e:
            print(f"Error creating staff payment: {e}")
            return (False, str(e))

    async def get_staff_name(self, staff_id: int) -> str:
        """Get staff member name by ID"""
        try:
            staff_list = await self.app_state.api_client.list_staff()
            for staff in staff_list:
                if staff.id_staff == staff_id:
                    return f"{staff.first_name} {staff.last_name}"
            return "Unknown"
        except Exception:
            return "Unknown"
