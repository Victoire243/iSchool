"""
Cash Register Dialogs Module
Handles dialog creation and management for cash register operations
"""

from flet import *  # type: ignore
from core import Constants
from datetime import datetime


class CashRegisterDialogs:
    """Handles dialog creation for cash register screen"""

    def __init__(self, screen):
        self.screen = screen
        self.edit_dialog = None
        self.delete_dialog = None

    def build_all_dialogs(self):
        """Build all dialogs"""
        self._build_edit_dialog()
        self._build_delete_dialog()

    def _build_edit_dialog(self):
        """Build edit dialog for cash register entries"""
        # Fields for editing
        self.edit_entry_type = Dropdown(
            label=self.screen.get_text("entry_type"),
            options=[
                DropdownOption(key="Entrée", text=self.screen.get_text("income")),
                DropdownOption(key="Sortie", text=self.screen.get_text("expense")),
            ],
            dense=True,
        )

        self.edit_date = TextField(
            label=self.screen.get_text("date"),
            hint_text="YYYY-MM-DD",
            dense=True,
            keyboard_type=KeyboardType.DATETIME,
        )

        self.edit_description = TextField(
            label=self.screen.get_text("description"),
            multiline=True,
            min_lines=2,
            max_lines=4,
            dense=True,
        )

        self.edit_amount = TextField(
            label=self.screen.get_text("amount"),
            keyboard_type=KeyboardType.NUMBER,
            suffix_text="FC",
            dense=True,
        )

        # Create dialog
        self.edit_dialog = AlertDialog(
            title=Text(self.screen.get_text("edit_entry")),
            content=Container(
                content=Column(
                    controls=[
                        self.edit_entry_type,
                        self.edit_date,
                        self.edit_description,
                        self.edit_amount,
                    ],
                    spacing=15,
                    tight=True,
                ),
                width=500,
            ),
            actions=[
                TextButton(
                    text=self.screen.get_text("cancel"),
                    on_click=self._close_edit_dialog,
                ),
                ElevatedButton(
                    text=self.screen.get_text("save"),
                    style=ButtonStyle(bgcolor=Constants.PRIMARY_COLOR, color="white"),
                    on_click=self._save_edited_entry,
                ),
            ],
            actions_alignment=MainAxisAlignment.END,
        )

    def _build_delete_dialog(self):
        """Build delete confirmation dialog"""
        self.delete_confirmation_text = Text("")

        self.delete_dialog = AlertDialog(
            title=Text(self.screen.get_text("confirm_deletion")),
            content=self.delete_confirmation_text,
            actions=[
                TextButton(
                    text=self.screen.get_text("cancel"),
                    on_click=self._close_delete_dialog,
                ),
                ElevatedButton(
                    text=self.screen.get_text("delete"),
                    style=ButtonStyle(bgcolor=Colors.RED, color="white"),
                    on_click=self._confirm_delete_entry,
                ),
            ],
            actions_alignment=MainAxisAlignment.END,
        )

    def open_entry_edit_dialog(self, entry):
        """Open edit dialog for a cash register entry"""
        self.current_entry = entry

        # Populate fields
        self.edit_entry_type.value = entry.type
        self.edit_date.value = entry.date
        self.edit_description.value = entry.description
        self.edit_amount.value = str(entry.amount)

        # Show dialog
        self.screen.page.overlay.append(self.edit_dialog)
        self.edit_dialog.open = True
        self.screen.page.update()

    def _close_edit_dialog(self, e):
        """Close edit dialog"""
        self.edit_dialog.open = False
        self.screen.page.update()

    async def _save_edited_entry(self, e):
        """Save edited entry"""
        try:
            amount = float(self.edit_amount.value)
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

        success = await self.screen.form_handlers.submit_edit_form(
            id_cash=self.current_entry.id_cash,
            school_year_id=self.current_entry.school_year_id,
            date=self.edit_date.value,
            entry_type=self.edit_entry_type.value,
            description=self.edit_description.value,
            amount=amount,
            user_id=self.current_entry.user_id,
        )

        if success:
            self._close_edit_dialog(e)

    def open_entry_delete_dialog(self, entry):
        """Open delete confirmation dialog"""
        self.current_entry = entry
        self.delete_confirmation_text.value = (
            f"{self.screen.get_text('delete_entry_confirm')}\n\n"
            f"{self.screen.get_text('description')}: {entry.description}\n"
            f"{self.screen.get_text('amount')}: {entry.amount} FC\n"
            f"{self.screen.get_text('date')}: {entry.date}"
        )

        # Show dialog
        self.screen.page.overlay.append(self.delete_dialog)
        self.delete_dialog.open = True
        self.screen.page.update()

    def _close_delete_dialog(self, e):
        """Close delete dialog"""
        self.delete_dialog.open = False
        self.screen.page.update()

    async def _confirm_delete_entry(self, e):
        """Confirm and delete entry"""
        success = await self.screen.form_handlers.delete_entry(
            self.current_entry.id_cash
        )

        if success:
            self._close_delete_dialog(e)
