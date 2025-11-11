"""
Checkout Dialogs Module
Contains dialog builders for the checkout screen
"""

from flet import *  # type: ignore
from core import Constants
from datetime import datetime


class CheckoutDialogs:
    """Dialog builders for checkout operations"""

    def __init__(self, checkout_screen):
        self.screen = checkout_screen

    def build_transaction_details_dialog(self, entry) -> AlertDialog:
        """Build dialog to show transaction details"""
        is_entry = entry.type.lower() == "entrée"
        color = Colors.GREEN if is_entry else Colors.RED

        return AlertDialog(
            modal=True,
            title=Row(
                controls=[
                    Icon(
                        Icons.ARROW_DOWNWARD if is_entry else Icons.ARROW_UPWARD,
                        color=color,
                    ),
                    Text(
                        self.screen.get_text("transaction_details"),
                        weight=FontWeight.BOLD,
                    ),
                ],
                spacing=10,
            ),
            content=Container(
                content=Column(
                    controls=[
                        self._build_detail_row(
                            self.screen.get_text("transaction_type"),
                            entry.type,
                            color,
                        ),
                        Divider(height=1),
                        self._build_detail_row(
                            self.screen.get_text("date"), entry.date
                        ),
                        Divider(height=1),
                        self._build_detail_row(
                            self.screen.get_text("transaction_description"),
                            entry.description,
                        ),
                        Divider(height=1),
                        self._build_detail_row(
                            self.screen.get_text("amount"),
                            f"$ {entry.amount:,.0f}",
                            color,
                        ),
                    ],
                    tight=True,
                    spacing=10,
                ),
                width=400,
            ),
            actions=[
                TextButton(
                    content=self.screen.get_text("print_receipt"),
                    icon=Icons.PRINT,
                    on_click=lambda e: self.screen.print_receipt(entry),
                ),
                TextButton(
                    content=self.screen.get_text("close"),
                    icon=Icons.CLOSE,
                    on_click=lambda e: self.screen.close_dialog(),
                ),
            ],
            actions_alignment=MainAxisAlignment.SPACE_BETWEEN,
            scrollable=True,
        )

    def build_receipt_dialog(self, entry) -> AlertDialog:
        """Build dialog to show printable receipt"""
        is_entry = entry.type.lower() == "entrée"

        receipt_content = f"""
═══════════════════════════════════
            REÇU DE CAISSE
═══════════════════════════════════

Date: {entry.date}
Heure: {datetime.now().strftime("%H:%M:%S")}

Type: {entry.type}
Description: {entry.description}

Montant: $ {entry.amount:,.0f}

═══════════════════════════════════
        Merci de votre confiance
═══════════════════════════════════
        """

        return AlertDialog(
            modal=True,
            title=Row(
                controls=[
                    Icon(Icons.RECEIPT_LONG, color=Constants.PRIMARY_COLOR),
                    Text(
                        self.screen.get_text("receipt_preview"),
                        weight=FontWeight.BOLD,
                    ),
                ],
                spacing=10,
            ),
            content=Container(
                content=Column(
                    controls=[
                        Container(
                            content=Text(
                                receipt_content,
                                font_family="Courier New",
                                size=12,
                                selectable=True,
                            ),
                            bgcolor=Colors.WHITE,
                            padding=Padding.all(15),
                            border=Border.all(1, Colors.GREY_300),
                            border_radius=BorderRadius.all(5),
                        ),
                        Container(height=10),
                        Text(
                            self.screen.get_text("receipt_hint"),
                            size=12,
                            color=Colors.GREY_600,
                            italic=True,
                        ),
                    ],
                    tight=True,
                    spacing=10,
                ),
                width=450,
            ),
            actions=[
                TextButton(
                    content=self.screen.get_text("close"),
                    on_click=lambda e: self.screen.close_dialog(),
                ),
            ],
            actions_alignment=MainAxisAlignment.END,
        )

    def build_confirmation_dialog(
        self, title: str, message: str, on_confirm
    ) -> AlertDialog:
        """Build a confirmation dialog"""
        return AlertDialog(
            modal=True,
            title=Row(
                controls=[
                    Icon(Icons.WARNING, color=Colors.ORANGE),
                    Text(title, weight=FontWeight.BOLD),
                ],
                spacing=10,
            ),
            content=Text(message),
            actions=[
                TextButton(
                    text=self.screen.get_text("cancel"),
                    on_click=lambda e: self.screen.close_dialog(),
                ),
                Button(
                    content=Text(self.screen.get_text("confirm")),
                    style=ButtonStyle(
                        bgcolor=Constants.PRIMARY_COLOR,
                        color="white",
                    ),
                    on_click=on_confirm,
                ),
            ],
            actions_alignment=MainAxisAlignment.SPACE_BETWEEN,
        )

    def build_success_dialog(self, message: str) -> AlertDialog:
        """Build a success dialog"""
        return AlertDialog(
            modal=True,
            title=Row(
                controls=[
                    Icon(Icons.CHECK_CIRCLE, color=Colors.GREEN),
                    Text(
                        self.screen.get_text("success"),
                        weight=FontWeight.BOLD,
                    ),
                ],
                spacing=10,
            ),
            content=Text(message),
            actions=[
                Button(
                    content=Text(self.screen.get_text("ok")),
                    style=ButtonStyle(
                        bgcolor=Colors.GREEN,
                        color="white",
                    ),
                    on_click=lambda e: self.screen.close_dialog(),
                ),
            ],
            actions_alignment=MainAxisAlignment.CENTER,
        )

    def build_error_dialog(self, message: str) -> AlertDialog:
        """Build an error dialog"""
        return AlertDialog(
            modal=True,
            title=Row(
                controls=[
                    Icon(Icons.ERROR, color=Colors.RED),
                    Text(
                        self.screen.get_text("error"),
                        weight=FontWeight.BOLD,
                    ),
                ],
                spacing=10,
            ),
            content=Text(message),
            actions=[
                Button(
                    content=Text(self.screen.get_text("ok")),
                    style=ButtonStyle(
                        bgcolor=Colors.RED,
                        color="white",
                    ),
                    on_click=lambda e: self.screen.close_dialog(),
                ),
            ],
            actions_alignment=MainAxisAlignment.CENTER,
        )

    def _build_detail_row(self, label: str, value: str, color=None) -> Row:
        """Build a detail row for dialogs"""
        return Row(
            controls=[
                Text(
                    f"{label}:",
                    weight=FontWeight.BOLD,
                    size=14,
                    color=Colors.GREY_700,
                ),
                Text(
                    value,
                    size=14,
                    weight=FontWeight.W_500,
                    color=color if color else Colors.BLACK,
                ),
            ],
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            wrap=True,
        )
