"""
Cash Register Form Handlers Module
Handles form submission logic for cash register operations
"""

import asyncio
from datetime import datetime
from flet import *  # type: ignore


class CashRegisterFormHandlers:
    """Handles form submissions for cash register screen"""

    def __init__(self, screen):
        self.screen = screen

    async def submit_entry_form(self, e: Event):
        """Submit quick entry form"""
        forms = self.screen.forms
        
        # Validate inputs
        if not forms.entry_description_field.value:
            self.screen.page.snack_bar = SnackBar(
                content=Text(self.screen.get_text("description_required")),
                bgcolor=Colors.RED,
            )
            self.screen.page.snack_bar.open = True
            self.screen.page.update()
            return

        if not forms.entry_amount_field.value:
            self.screen.page.snack_bar = SnackBar(
                content=Text(self.screen.get_text("amount_required")),
                bgcolor=Colors.RED,
            )
            self.screen.page.snack_bar.open = True
            self.screen.page.update()
            return

        try:
            amount = float(forms.entry_amount_field.value)
            if amount <= 0:
                raise ValueError("Amount must be positive")
        except ValueError:
            self.screen.page.snack_bar = SnackBar(
                content=Text(self.screen.get_text("invalid_amount")),
                bgcolor=Colors.RED,
            )
            self.screen.page.snack_bar.open = True
            self.screen.page.update()
            return

        # Get active school year
        active_school_year = await self.screen.app_state.api_client.get_active_school_year()
        if not active_school_year:
            self.screen.page.snack_bar = SnackBar(
                content=Text(self.screen.get_text("no_active_school_year")),
                bgcolor=Colors.RED,
            )
            self.screen.page.snack_bar.open = True
            self.screen.page.update()
            return

        # Create entry
        success, entry = await self.screen.services.create_entry(
            school_year_id=active_school_year.id_school_year,
            date=forms.entry_date_field.value,
            entry_type=forms.entry_type_dropdown.value,
            description=forms.entry_description_field.value,
            amount=amount,
            user_id=self.screen.app_state.current_user.id_user,
        )

        if success:
            self.screen.page.snack_bar = SnackBar(
                content=Text(self.screen.get_text("entry_created_success")),
                bgcolor=Colors.GREEN,
            )
            self.screen.page.snack_bar.open = True
            self.screen.page.update()

            # Clear form and reload data
            forms.clear_all_forms()
            await self.screen.load_data()
        else:
            self.screen.page.snack_bar = SnackBar(
                content=Text(self.screen.get_text("entry_creation_failed")),
                bgcolor=Colors.RED,
            )
            self.screen.page.snack_bar.open = True
            self.screen.page.update()

    async def submit_staff_payment_form(self, e: Event):
        """Submit staff payment form"""
        forms = self.screen.forms
        
        # Validate inputs
        if not forms.staff_dropdown.value:
            self.screen.page.snack_bar = SnackBar(
                content=Text(self.screen.get_text("staff_required")),
                bgcolor=Colors.RED,
            )
            self.screen.page.snack_bar.open = True
            self.screen.page.update()
            return

        if not forms.staff_payment_amount_field.value:
            self.screen.page.snack_bar = SnackBar(
                content=Text(self.screen.get_text("amount_required")),
                bgcolor=Colors.RED,
            )
            self.screen.page.snack_bar.open = True
            self.screen.page.update()
            return

        try:
            amount = float(forms.staff_payment_amount_field.value)
            if amount <= 0:
                raise ValueError("Amount must be positive")
        except ValueError:
            self.screen.page.snack_bar = SnackBar(
                content=Text(self.screen.get_text("invalid_amount")),
                bgcolor=Colors.RED,
            )
            self.screen.page.snack_bar.open = True
            self.screen.page.update()
            return

        # Get active school year
        active_school_year = await self.screen.app_state.api_client.get_active_school_year()
        if not active_school_year:
            self.screen.page.snack_bar = SnackBar(
                content=Text(self.screen.get_text("no_active_school_year")),
                bgcolor=Colors.RED,
            )
            self.screen.page.snack_bar.open = True
            self.screen.page.update()
            return

        # Get staff name for description
        staff_id = int(forms.staff_dropdown.value)
        staff_name = forms.staff_dropdown.options[
            [opt.key for opt in forms.staff_dropdown.options].index(str(staff_id))
        ].text

        # Create cash register entry for staff payment (Sortie)
        success, entry = await self.screen.services.create_entry(
            school_year_id=active_school_year.id_school_year,
            date=forms.staff_payment_date_field.value,
            entry_type="Sortie",
            description=f"Paiement du personnel: {staff_name}",
            amount=amount,
            user_id=self.screen.app_state.current_user.id_user,
        )

        if success:
            self.screen.page.snack_bar = SnackBar(
                content=Text(self.screen.get_text("staff_payment_success")),
                bgcolor=Colors.GREEN,
            )
            self.screen.page.snack_bar.open = True
            self.screen.page.update()

            # Clear form and reload data
            forms.clear_all_forms()
            await self.screen.load_data()
        else:
            self.screen.page.snack_bar = SnackBar(
                content=Text(self.screen.get_text("staff_payment_failed")),
                bgcolor=Colors.RED,
            )
            self.screen.page.snack_bar.open = True
            self.screen.page.update()

    async def submit_edit_form(
        self,
        id_cash: int,
        school_year_id: int,
        date: str,
        entry_type: str,
        description: str,
        amount: float,
        user_id: int,
    ):
        """Submit edit form for cash register entry"""
        success = await self.screen.services.update_entry(
            id_cash=id_cash,
            school_year_id=school_year_id,
            date=date,
            entry_type=entry_type,
            description=description,
            amount=amount,
            user_id=user_id,
        )

        if success:
            self.screen.page.snack_bar = SnackBar(
                content=Text(self.screen.get_text("entry_updated_success")),
                bgcolor=Colors.GREEN,
            )
            await self.screen.load_data()
        else:
            self.screen.page.snack_bar = SnackBar(
                content=Text(self.screen.get_text("entry_update_failed")),
                bgcolor=Colors.RED,
            )
        
        self.screen.page.snack_bar.open = True
        self.screen.page.update()
        return success

    async def delete_entry(self, id_cash: int):
        """Delete a cash register entry"""
        success = await self.screen.services.delete_entry(id_cash)

        if success:
            self.screen.page.snack_bar = SnackBar(
                content=Text(self.screen.get_text("entry_deleted_success")),
                bgcolor=Colors.GREEN,
            )
            await self.screen.load_data()
        else:
            self.screen.page.snack_bar = SnackBar(
                content=Text(self.screen.get_text("entry_deletion_failed")),
                bgcolor=Colors.RED,
            )
        
        self.screen.page.snack_bar.open = True
        self.screen.page.update()
        return success
