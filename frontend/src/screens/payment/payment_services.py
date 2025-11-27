import asyncio
from core import AppState


class PaymentServices:
    def __init__(self, app_state: AppState):
        self.app_state = app_state

    async def load_students_data(self):
        """Load all students data"""
        return (True, await self.app_state.api_client.list_students())

    async def load_classrooms_data(self):
        """Load all classrooms data"""
        return (True, await self.app_state.api_client.list_classrooms())

    async def load_enrollments_data(self):
        """Load all enrollments data"""
        return (True, await self.app_state.api_client.list_enrollments())

    async def search_students(self, query: str):
        """Search students by name"""
        return await self.app_state.api_client.search_students(query)

    async def load_payments_data(self):
        """Load all payments data"""
        return (True, await self.app_state.api_client.list_payments())

    async def load_payment_types_data(self):
        """Load all payment types data (now loading fees)"""
        # Load fees instead of payment_types
        fees = await self.app_state.api_client.list_fees()
        # Filter only active fees
        active_fees = [fee for fee in fees if fee.is_active]
        return (True, active_fees)

    async def create_payment(self, payment_data: dict):
        """Create a new payment"""
        # TODO: Implement create_payment in API client
        await asyncio.sleep(0.5)  # Simulate API call
        return True
