"""
Checkout Form Handlers Module
Handles form submissions for the checkout screen
"""

import asyncio
from flet import *  # type: ignore
from core import Constants


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
            # Validate inputs - now using selected_staff_id instead of dropdown
            staff_id = self.screen.selected_staff_id
            amount_str = self.screen.staff_payment_amount_field.value

            if not staff_id:
                self.screen.show_error_dialog(
                    self.screen.get_text("staff_selection_required")
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
                self.clear_staff_search(None)
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

    # ========================================================================
    # STAFF SEARCH METHODS (similar to student search in payment screen)
    # ========================================================================

    def handle_staff_search_change(self, e):
        """Handle changes in staff search field"""
        from utils import Utils

        search_text = e.control.value.strip()

        # Hide suggestions if less than 2 characters
        if len(search_text) < 2:
            self.screen.suggestions_container_staff.visible = False
            if hasattr(self.screen.suggestions_container_staff, "update"):
                self.screen.suggestions_container_staff.update()
            return

        # Filter staff based on search text
        suggestions = []
        if self.screen.staff_list:
            normalized_search = Utils.normalize_text(search_text.lower())

            for staff in self.screen.staff_list:
                # Get staff info
                first_name = staff.first_name or ""
                last_name = staff.last_name or ""
                position = staff.position or ""
                full_name = f"{first_name} {last_name}".strip()

                # Normalize for comparison
                normalized_full_name = Utils.normalize_text(full_name.lower())
                normalized_first = Utils.normalize_text(first_name.lower())
                normalized_last = Utils.normalize_text(last_name.lower())
                normalized_position = Utils.normalize_text(position.lower())

                # Check if search text matches any part
                if (
                    normalized_search in normalized_full_name
                    or normalized_search in normalized_first
                    or normalized_search in normalized_last
                    or normalized_search in normalized_position
                ):
                    suggestions.append(staff)

        # Display suggestions
        self.display_staff_suggestions(suggestions)

    def display_staff_suggestions(self, suggestions):
        """Display the list of staff suggestions"""
        if not suggestions:
            self.screen.suggestions_container_staff.visible = False
            if hasattr(self.screen.suggestions_container_staff, "update"):
                self.screen.suggestions_container_staff.update()
            return

        # Create suggestion widgets
        suggestion_widgets = []
        for staff in suggestions[:10]:  # Limit to 10 suggestions
            # Create full name
            full_name = f"{staff.first_name} {staff.last_name}".strip()

            # Create suggestion tile
            suggestion_tile = ListTile(
                title=Text(full_name, weight=FontWeight.BOLD),
                subtitle=Text(
                    f"Poste: {staff.position} | Salaire: {staff.salary_base:,.0f} FC",
                    size=12,
                ),
                leading=Icon(
                    Icons.PERSON,
                    color=Constants.PRIMARY_COLOR,
                ),
                on_click=lambda e, s=staff: self.select_staff(s),
                bgcolor=Colors.TRANSPARENT,
                hover_color=Colors.BLUE_50,
            )
            suggestion_widgets.append(suggestion_tile)

        # Update suggestions container
        self.screen.suggestions_container_staff.content = ListView(
            controls=suggestion_widgets,
            auto_scroll=False,
            spacing=2,
            expand=True,
        )
        self.screen.suggestions_container_staff.visible = True
        if hasattr(self.screen.suggestions_container_staff, "update"):
            self.screen.suggestions_container_staff.update()

    def select_staff(self, staff):
        """Select a staff member from suggestions"""
        self.screen.selected_staff_id = staff.id_staff

        # Build display text for search field
        full_name = f"{staff.first_name} {staff.last_name}".strip()
        display_text = f"{full_name} - {staff.position}"

        self.screen.staff_search_field.value = display_text

        # Update staff info display
        self.screen.staff_position_text_info.value = f"Poste: {staff.position}"
        self.screen.staff_contact_text_info.value = (
            f"Salaire de base: {staff.salary_base:,.0f} FC"
        )

        # Hide suggestions
        self.screen.suggestions_container_staff.visible = False

        # Update interface
        if hasattr(self.screen.staff_search_field, "update"):
            self.screen.staff_search_field.update()
        if hasattr(self.screen.suggestions_container_staff, "update"):
            self.screen.suggestions_container_staff.update()
        if hasattr(self.screen.staff_position_text_info, "update"):
            self.screen.staff_position_text_info.update()
        if hasattr(self.screen.staff_contact_text_info, "update"):
            self.screen.staff_contact_text_info.update()

    def clear_staff_search(self, e):
        """Clear staff search"""
        self.screen.selected_staff_id = None
        self.screen.staff_search_field.value = ""
        self.screen.staff_position_text_info.value = ""
        self.screen.staff_contact_text_info.value = ""
        self.screen.suggestions_container_staff.visible = False

        # Update interface
        if hasattr(self.screen.staff_search_field, "update"):
            self.screen.staff_search_field.update()
        if hasattr(self.screen.suggestions_container_staff, "update"):
            self.screen.suggestions_container_staff.update()
        if hasattr(self.screen.staff_position_text_info, "update"):
            self.screen.staff_position_text_info.update()
        if hasattr(self.screen.staff_contact_text_info, "update"):
            self.screen.staff_contact_text_info.update()
