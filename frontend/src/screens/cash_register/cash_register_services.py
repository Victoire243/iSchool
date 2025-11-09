"""
Cash Register Services Module
Handles data fetching and business logic for cash register operations
"""

import asyncio
from typing import Dict, List, Optional
from datetime import datetime
from core import AppState
from models import CashRegisterModel


class CashRegisterServices:
    """Service class for cash register operations"""

    def __init__(self, app_state: AppState):
        self.app_state = app_state

    async def load_cash_register_entries(self) -> tuple[bool, List[CashRegisterModel]]:
        """Load all cash register entries"""
        try:
            entries = await self.app_state.api_client.list_cash_register_entries()
            return (True, entries)
        except Exception as e:
            print(f"Error loading cash register entries: {e}")
            return (False, [])

    async def filter_entries(
        self, start_date: str = None, end_date: str = None, entry_type: str = None
    ) -> tuple[bool, List[CashRegisterModel]]:
        """Filter cash register entries by criteria"""
        try:
            entries = await self.app_state.api_client.filter_cash_register_entries(
                start_date=start_date, end_date=end_date, entry_type=entry_type
            )
            return (True, entries)
        except Exception as e:
            print(f"Error filtering cash register entries: {e}")
            return (False, [])

    async def get_statistics(self) -> tuple[bool, Dict[str, float]]:
        """Get cash register statistics"""
        try:
            stats = await self.app_state.api_client.get_cash_register_statistics()
            return (True, stats)
        except Exception as e:
            print(f"Error loading statistics: {e}")
            return (False, {})

    async def create_entry(
        self,
        school_year_id: int,
        date: str,
        entry_type: str,
        description: str,
        amount: float,
        user_id: int,
    ) -> tuple[bool, Optional[CashRegisterModel]]:
        """Create a new cash register entry"""
        try:
            entry = await self.app_state.api_client.create_cash_register_entry(
                school_year_id=school_year_id,
                date=date,
                entry_type=entry_type,
                description=description,
                amount=amount,
                user_id=user_id,
            )
            return (True, entry)
        except Exception as e:
            print(f"Error creating entry: {e}")
            return (False, None)

    async def update_entry(
        self,
        id_cash: int,
        school_year_id: int,
        date: str,
        entry_type: str,
        description: str,
        amount: float,
        user_id: int,
    ) -> bool:
        """Update an existing cash register entry"""
        try:
            success = await self.app_state.api_client.update_cash_register_entry(
                id_cash=id_cash,
                school_year_id=school_year_id,
                date=date,
                entry_type=entry_type,
                description=description,
                amount=amount,
                user_id=user_id,
            )
            return success
        except Exception as e:
            print(f"Error updating entry: {e}")
            return False

    async def delete_entry(self, id_cash: int) -> bool:
        """Delete a cash register entry"""
        try:
            success = await self.app_state.api_client.delete_cash_register_entry(
                id_cash=id_cash
            )
            return success
        except Exception as e:
            print(f"Error deleting entry: {e}")
            return False

    async def load_staff_list(self):
        """Load list of staff members for payment menu"""
        try:
            staff = await self.app_state.api_client.list_staff()
            return (True, staff)
        except Exception as e:
            print(f"Error loading staff: {e}")
            return (False, [])

    async def load_staff_payments(self):
        """Load staff payment records"""
        try:
            payments = await self.app_state.api_client.list_staff_payments()
            return (True, payments)
        except Exception as e:
            print(f"Error loading staff payments: {e}")
            return (False, [])

    def export_entries_to_csv(self, entries: List[CashRegisterModel]) -> str:
        """Export entries to CSV format"""
        import csv
        from io import StringIO
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(["ID", "Date", "Type", "Description", "Amount (FC)"])
        
        # Write data
        for entry in entries:
            writer.writerow([
                entry.id_cash,
                entry.date,
                entry.type,
                entry.description,
                entry.amount
            ])
        
        return output.getvalue()

    def get_monthly_summary(self, entries: List[CashRegisterModel]) -> dict:
        """Get monthly summary of entries"""
        from collections import defaultdict
        from datetime import datetime
        
        monthly_data = defaultdict(lambda: {"income": 0.0, "expense": 0.0})
        
        for entry in entries:
            try:
                date_obj = datetime.strptime(entry.date, "%Y-%m-%d")
                month_key = date_obj.strftime("%Y-%m")
                
                if entry.type == "Entrée":
                    monthly_data[month_key]["income"] += entry.amount
                else:
                    monthly_data[month_key]["expense"] += entry.amount
            except:
                continue
        
        return dict(monthly_data)
