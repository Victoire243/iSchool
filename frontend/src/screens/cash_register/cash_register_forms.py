"""
Cash Register Forms Module
Contains form components for cash register operations
"""

from flet import *  # type: ignore
from datetime import datetime
from core import Constants


class CashRegisterForms:
    """Handles form creation for cash register screen"""

    def __init__(self, screen):
        self.screen = screen
        self.build_forms()

    def build_forms(self):
        """Build all forms"""
        self._build_quick_entry_form()
        self._build_staff_payment_form()

    def _build_quick_entry_form(self):
        """Build quick entry form (for both income and expenses)"""
        # Entry type selector
        self.entry_type_dropdown = Dropdown(
            label=self.screen.get_text("entry_type"),
            options=[
                DropdownOption(key="Entrée", text=self.screen.get_text("income")),
                DropdownOption(key="Sortie", text=self.screen.get_text("expense")),
            ],
            value="Sortie",
            dense=True,
        )

        # Date picker
        self.entry_date_field = TextField(
            label=self.screen.get_text("date"),
            hint_text="YYYY-MM-DD",
            value=datetime.now().strftime("%Y-%m-%d"),
            dense=True,
            keyboard_type=KeyboardType.DATETIME,
        )

        # Description
        self.entry_description_field = TextField(
            label=self.screen.get_text("description"),
            hint_text=self.screen.get_text("enter_description"),
            multiline=True,
            min_lines=2,
            max_lines=4,
            dense=True,
        )

        # Amount
        self.entry_amount_field = TextField(
            label=self.screen.get_text("amount"),
            hint_text="0.00",
            keyboard_type=KeyboardType.NUMBER,
            suffix_text="FC",
            dense=True,
        )

        # Submit button
        self.submit_entry_button = ElevatedButton(
            text=self.screen.get_text("submit"),
            icon=Icons.SAVE,
            style=ButtonStyle(
                bgcolor=Constants.PRIMARY_COLOR,
                color="white",
                padding=Padding.symmetric(horizontal=30, vertical=15),
            ),
            on_click=self.screen.form_handlers.submit_entry_form,
        )

        # Clear button
        self.clear_entry_button = TextButton(
            text=self.screen.get_text("clear"),
            icon=Icons.CLEAR,
            on_click=self._clear_entry_form,
        )

        # Build the form container
        self.quick_entry_form_container = Column(
            controls=[
                Text(
                    self.screen.get_text("quick_entry"),
                    size=18,
                    weight=FontWeight.BOLD,
                    color=Constants.PRIMARY_COLOR,
                ),
                Divider(),
                self.entry_type_dropdown,
                self.entry_date_field,
                self.entry_description_field,
                self.entry_amount_field,
                Row(
                    controls=[
                        self.submit_entry_button,
                        self.clear_entry_button,
                    ],
                    alignment=MainAxisAlignment.END,
                    spacing=10,
                ),
            ],
            spacing=15,
        )

    def _build_staff_payment_form(self):
        """Build staff payment form"""
        # Staff selector
        self.staff_dropdown = Dropdown(
            label=self.screen.get_text("select_staff"),
            options=[],
            dense=True,
        )

        # Payment date
        self.staff_payment_date_field = TextField(
            label=self.screen.get_text("payment_date"),
            hint_text="YYYY-MM-DD",
            value=datetime.now().strftime("%Y-%m-%d"),
            dense=True,
            keyboard_type=KeyboardType.DATETIME,
        )

        # Payment amount
        self.staff_payment_amount_field = TextField(
            label=self.screen.get_text("amount"),
            hint_text="0.00",
            keyboard_type=KeyboardType.NUMBER,
            suffix_text="FC",
            dense=True,
        )

        # Submit button
        self.submit_staff_payment_button = ElevatedButton(
            text=self.screen.get_text("process_payment"),
            icon=Icons.PAYMENT,
            style=ButtonStyle(
                bgcolor=Constants.SECONDARY_COLOR,
                color="white",
                padding=Padding.symmetric(horizontal=30, vertical=15),
            ),
            on_click=self.screen.form_handlers.submit_staff_payment_form,
        )

        # Build the form container
        self.staff_payment_form_container = Column(
            controls=[
                Text(
                    self.screen.get_text("staff_payment"),
                    size=18,
                    weight=FontWeight.BOLD,
                    color=Constants.SECONDARY_COLOR,
                ),
                Divider(),
                self.staff_dropdown,
                self.staff_payment_date_field,
                self.staff_payment_amount_field,
                Row(
                    controls=[self.submit_staff_payment_button],
                    alignment=MainAxisAlignment.END,
                ),
            ],
            spacing=15,
        )

    def _clear_entry_form(self, e):
        """Clear the quick entry form"""
        self.entry_type_dropdown.value = "Sortie"
        self.entry_date_field.value = datetime.now().strftime("%Y-%m-%d")
        self.entry_description_field.value = ""
        self.entry_amount_field.value = ""
        
        self.entry_type_dropdown.update()
        self.entry_date_field.update()
        self.entry_description_field.update()
        self.entry_amount_field.update()

    def clear_all_forms(self):
        """Clear all forms"""
        self._clear_entry_form(None)
        
        # Clear staff payment form
        self.staff_dropdown.value = None
        self.staff_payment_date_field.value = datetime.now().strftime("%Y-%m-%d")
        self.staff_payment_amount_field.value = ""
        
        try:
            self.staff_dropdown.update()
            self.staff_payment_date_field.update()
            self.staff_payment_amount_field.update()
        except:
            pass

    def populate_staff_dropdown(self, staff_list):
        """Populate staff dropdown with staff members"""
        self.staff_dropdown.options = [
            DropdownOption(
                key=str(staff.id_staff),
                text=f"{staff.first_name} {staff.last_name}",
            )
            for staff in staff_list
        ]
        try:
            self.staff_dropdown.update()
        except:
            pass
