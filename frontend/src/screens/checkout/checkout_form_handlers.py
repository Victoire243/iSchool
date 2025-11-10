"""
Checkout Form Handlers Module
Handles form submissions for the checkout screen
"""

import asyncio
from flet import *  # type: ignore


class CheckoutFormHandlers:
    """Form submission handlers for checkout operations"""

    def __init__(self, checkout_screen):
        self.screen = checkout_screen

    async def handle_quick_entry_submit(self, e):
        """Handle quick cash entry form submission"""
        try:
            # Validate inputs
            description = self.screen.entry_description_field.value
            amount_str = self.screen.entry_amount_field.value
            entry_type = self.screen.entry_type_dropdown.value

            if not description or not description.strip():
                self.screen.show_error_dialog(
                    self.screen.get_text("description_required")
                )
                return

            if not amount_str or not amount_str.strip():
                self.screen.show_error_dialog(self.screen.get_text("amount_required"))
                return

            try:
                amount = float(amount_str.strip())
                if amount <= 0:
                    self.screen.show_error_dialog(
                        self.screen.get_text("amount_must_be_positive")
                    )
                    return
            except ValueError:
                self.screen.show_error_dialog(self.screen.get_text("invalid_amount"))
                return

            # Create entry
            success, result = await self.screen.services.create_quick_entry(
                description=description.strip(),
                amount=amount,
                entry_type=entry_type,
            )

            if success:
                self.screen.show_success_dialog(
                    self.screen.get_text("entry_created_successfully")
                )
                # Clear form
                self.screen.entry_description_field.value = ""
                self.screen.entry_amount_field.value = ""
                self.screen.entry_type_dropdown.value = "Entrée"
                # Hide form
                self.screen.toggle_quick_entry_form(None)
                # Reload data
                await self.screen.load_data()
            else:
                self.screen.show_error_dialog(
                    f"{self.screen.get_text('error_creating_entry')}: {result}"
                )

        except Exception as ex:
            print(f"Error in handle_quick_entry_submit: {ex}")
            self.screen.show_error_dialog(
                f"{self.screen.get_text('unexpected_error')}: {str(ex)}"
            )

    async def handle_quick_expense_submit(self, e):
        """Handle quick expense form submission"""
        try:
            # Validate inputs
            description = self.screen.expense_description_field.value
            amount_str = self.screen.expense_amount_field.value

            if not description or not description.strip():
                self.screen.show_error_dialog(
                    self.screen.get_text("description_required")
                )
                return

            if not amount_str or not amount_str.strip():
                self.screen.show_error_dialog(self.screen.get_text("amount_required"))
                return

            try:
                amount = float(amount_str.strip())
                if amount <= 0:
                    self.screen.show_error_dialog(
                        self.screen.get_text("amount_must_be_positive")
                    )
                    return
            except ValueError:
                self.screen.show_error_dialog(self.screen.get_text("invalid_amount"))
                return

            # Create expense
            success, result = await self.screen.services.create_quick_expense(
                description=description.strip(),
                amount=amount,
            )

            if success:
                self.screen.show_success_dialog(
                    self.screen.get_text("expense_created_successfully")
                )
                # Clear form
                self.screen.expense_description_field.value = ""
                self.screen.expense_amount_field.value = ""
                # Hide form
                self.screen.toggle_quick_expense_form(None)
                # Reload data
                await self.screen.load_data()
            else:
                self.screen.show_error_dialog(
                    f"{self.screen.get_text('error_creating_expense')}: {result}"
                )

        except Exception as ex:
            print(f"Error in handle_quick_expense_submit: {ex}")
            self.screen.show_error_dialog(
                f"{self.screen.get_text('unexpected_error')}: {str(ex)}"
            )

    async def handle_staff_payment_submit(self, e):
        """Handle staff payment form submission"""
        try:
            # Validate inputs
            staff_id_str = self.screen.staff_dropdown.value
            amount_str = self.screen.staff_payment_amount_field.value

            if not staff_id_str:
                self.screen.show_error_dialog(
                    self.screen.get_text("staff_selection_required")
                )
                return

            if not amount_str or not amount_str.strip():
                self.screen.show_error_dialog(self.screen.get_text("amount_required"))
                return

            try:
                staff_id = int(staff_id_str)
                amount = float(amount_str.strip())
                if amount <= 0:
                    self.screen.show_error_dialog(
                        self.screen.get_text("amount_must_be_positive")
                    )
                    return
            except ValueError:
                self.screen.show_error_dialog(
                    self.screen.get_text("invalid_input_values")
                )
                return

            # Create staff payment
            success, result = await self.screen.services.create_staff_payment(
                staff_id=staff_id,
                amount=amount,
            )

            if success:
                self.screen.show_success_dialog(
                    self.screen.get_text("staff_payment_created_successfully")
                )
                # Clear form
                self.screen.staff_dropdown.value = None
                self.screen.staff_payment_amount_field.value = ""
                # Hide form
                self.screen.toggle_staff_payment_form(None)
                # Reload data
                await self.screen.load_data()
            else:
                self.screen.show_error_dialog(
                    f"{self.screen.get_text('error_creating_staff_payment')}: {result}"
                )

        except Exception as ex:
            print(f"Error in handle_staff_payment_submit: {ex}")
            self.screen.show_error_dialog(
                f"{self.screen.get_text('unexpected_error')}: {str(ex)}"
            )
