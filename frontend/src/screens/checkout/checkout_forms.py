"""
Checkout Forms Module
Contains all form builders for the checkout screen
"""

from flet import *  # type: ignore
from core import Constants
from datetime import datetime


class CheckoutForms:
    """Form builders for checkout operations"""

    def __init__(self, checkout_screen):
        self.screen = checkout_screen

    def build_quick_entry_form(self) -> Column:
        """Build form for quick cash register entry"""
        self.screen.entry_description_field = TextField(
            label=self.screen.get_text("description_quick_entry"),
            hint_text=self.screen.get_text("enter_description"),
            border_color=Constants.PRIMARY_COLOR,
            expand=True,
        )

        self.screen.entry_amount_field = TextField(
            label=self.screen.get_text("amount"),
            hint_text=self.screen.get_text("enter_amount"),
            keyboard_type=KeyboardType.NUMBER,
            border_color=Constants.PRIMARY_COLOR,
            suffix=Text(f" {Constants.DEVISE}"),
            expand=True,
        )

        self.screen.entry_type_dropdown = Dropdown(
            label=self.screen.get_text("transaction_type"),
            hint_text=self.screen.get_text("select_type"),
            border_color=Constants.PRIMARY_COLOR,
            options=[
                dropdown.Option("entry", self.screen.get_text("entry")),
                # dropdown.Option("Sortie", self.screen.get_text("exit")),
            ],
            value="entry",
            expand=True,
        )

        return Column(
            controls=[
                Row(
                    controls=[
                        self.screen.entry_type_dropdown,
                    ],
                ),
                Row(
                    controls=[
                        self.screen.entry_description_field,
                    ],
                ),
                Row(
                    controls=[
                        self.screen.entry_amount_field,
                    ],
                ),
                Row(
                    controls=[
                        Button(
                            content=self.screen.get_text("submit"),
                            icon=Icons.SAVE,
                            style=ButtonStyle(
                                shape=RoundedRectangleBorder(radius=5),
                                bgcolor=Constants.PRIMARY_COLOR,
                                padding=Padding(10, 20, 10, 20),
                                color="white",
                            ),
                            on_click=self.screen.form_handlers.handle_quick_entry_submit,
                        ),
                        Button(
                            content=self.screen.get_text("cancel"),
                            icon=Icons.CANCEL,
                            style=ButtonStyle(
                                shape=RoundedRectangleBorder(radius=5),
                                bgcolor=Constants.CANCEL_COLOR,
                                padding=Padding(10, 20, 10, 20),
                                color="white",
                            ),
                            on_click=self.screen.toggle_quick_entry_form,
                        ),
                    ],
                    alignment=MainAxisAlignment.END,
                    spacing=10,
                ),
            ],
            spacing=15,
        )

    def build_quick_expense_form(self) -> Column:
        """Build form for quick expense"""
        self.screen.expense_description_field = TextField(
            label=self.screen.get_text("description_quick_expense"),
            hint_text=self.screen.get_text("enter_expense_description"),
            border_color=Constants.PRIMARY_COLOR,
            expand=True,
            multiline=True,
            min_lines=2,
            max_lines=4,
        )

        self.screen.expense_amount_field = TextField(
            label=self.screen.get_text("amount"),
            hint_text=self.screen.get_text("enter_amount"),
            keyboard_type=KeyboardType.NUMBER,
            border_color=Constants.PRIMARY_COLOR,
            suffix=Text(f"{Constants.DEVISE} "),
            expand=True,
        )

        return Column(
            controls=[
                Row(
                    controls=[
                        self.screen.expense_description_field,
                    ],
                ),
                Row(
                    controls=[
                        self.screen.expense_amount_field,
                    ],
                ),
                Row(
                    controls=[
                        Button(
                            content=self.screen.get_text("submit"),
                            icon=Icons.SHOPPING_CART,
                            style=ButtonStyle(
                                shape=RoundedRectangleBorder(radius=5),
                                bgcolor=Constants.PRIMARY_COLOR,
                                padding=Padding(10, 20, 10, 20),
                                color="white",
                            ),
                            on_click=self.screen.form_handlers.handle_quick_expense_submit,
                        ),
                        Button(
                            content=self.screen.get_text("cancel"),
                            icon=Icons.CANCEL,
                            style=ButtonStyle(
                                shape=RoundedRectangleBorder(radius=5),
                                bgcolor=Constants.CANCEL_COLOR,
                                padding=Padding(10, 20, 10, 20),
                                color="white",
                            ),
                            on_click=self.screen.toggle_quick_expense_form,
                        ),
                    ],
                    alignment=MainAxisAlignment.END,
                    spacing=10,
                ),
            ],
            spacing=15,
        )

    def build_staff_payment_form(self) -> Column:
        """Build form for staff payment"""
        # Staff search field with suggestions
        self.screen.staff_search_field = TextField(
            label=self.screen.get_text("search_staff"),
            hint_text=self.screen.get_text("enter_staff_name"),
            on_change=self.screen.form_handlers.handle_staff_search_change,
            prefix_icon=Icons.SEARCH,
            suffix=IconButton(
                icon=Icons.CLEAR,
                tooltip=self.screen.get_text("clear"),
                on_click=self.screen.form_handlers.clear_staff_search,
            ),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=True,
        )

        # Container for staff suggestions
        self.screen.suggestions_container_staff = Container(
            visible=False,
            width=400,
            height=250,
            bgcolor=Colors.WHITE,
            border=Border.all(1, Colors.GREY_300),
            border_radius=BorderRadius.all(5),
            padding=Padding.all(5),
        )

        # Staff info display
        self.screen.staff_position_text_info = Text(
            value="",
            size=14,
            color=Constants.PRIMARY_COLOR,
        )

        self.screen.staff_contact_text_info = Text(
            value="",
            size=14,
            color=Constants.PRIMARY_COLOR,
        )

        self.screen.staff_payment_amount_field = TextField(
            label=self.screen.get_text("payment_amount"),
            hint_text=self.screen.get_text("enter_payment_amount"),
            keyboard_type=KeyboardType.NUMBER,
            border_color=Constants.PRIMARY_COLOR,
            suffix=Text(f"{Constants.DEVISE} "),
            expand=True,
        )

        self.screen.staff_payment_date_field = TextField(
            label=self.screen.get_text("payment_date"),
            hint_text=self.screen.get_text("payment_date_hint"),
            border_color=Constants.PRIMARY_COLOR,
            value=datetime.now().strftime("%d-%m-%Y"),
            read_only=True,
            expand=True,
        )

        return Column(
            controls=[
                Column(
                    controls=[
                        self.screen.staff_search_field,
                        self.screen.suggestions_container_staff,
                    ],
                ),
                Row(
                    controls=[
                        self.screen.staff_position_text_info,
                        self.screen.staff_contact_text_info,
                    ],
                    spacing=20,
                ),
                Row(
                    controls=[
                        self.screen.staff_payment_amount_field,
                        self.screen.staff_payment_date_field,
                    ],
                    spacing=10,
                ),
                Row(
                    controls=[
                        Button(
                            content=self.screen.get_text("pay_staff"),
                            icon=Icons.PAYMENTS,
                            style=ButtonStyle(
                                shape=RoundedRectangleBorder(radius=5),
                                bgcolor=Constants.PRIMARY_COLOR,
                                padding=Padding(10, 20, 10, 20),
                                color="white",
                            ),
                            on_click=self.screen.form_handlers.handle_staff_payment_submit,
                        ),
                        Button(
                            content=self.screen.get_text("cancel"),
                            icon=Icons.CANCEL,
                            style=ButtonStyle(
                                shape=RoundedRectangleBorder(radius=5),
                                bgcolor=Constants.CANCEL_COLOR,
                                padding=Padding(10, 20, 10, 20),
                                color="white",
                            ),
                            on_click=self.screen.toggle_staff_payment_form,
                        ),
                    ],
                    alignment=MainAxisAlignment.END,
                    spacing=10,
                ),
            ],
            spacing=15,
        )

    # Removed populate_staff_dropdown method as we now use search
