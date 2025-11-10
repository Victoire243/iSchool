"""
Checkout Components Module
Contains reusable UI components for the checkout screen
"""

from flet import *  # type: ignore
from core import Constants


class CheckoutComponents:
    """Utility class for creating checkout UI components"""

    @staticmethod
    def get_box_style() -> dict:
        """Return common box styling"""
        return {
            "border_radius": BorderRadius.all(10),
            "shadow": BoxShadow(color="black12", blur_radius=5, offset=Offset(0, 2)),
            "bgcolor": "#f8faff",
        }

    @staticmethod
    def get_color_by_entry_type(entry_type: str) -> ColorValue:
        """Get color based on entry type"""
        if entry_type.lower() == "entrée" or entry_type.lower() == "entry":
            return Colors.GREEN
        elif entry_type.lower() == "sortie" or entry_type.lower() == "exit":
            return Colors.RED
        return Colors.GREY

    @staticmethod
    def create_stat_card(
        title: str,
        value: str,
        icon: str,
        color: str,
        subtitle: str = None,
        on_click=None,
    ) -> Control:
        """Create a statistics card"""
        card_content = Row(
            controls=[
                Icon(icon, color=color, size=40),
                Column(
                    controls=[
                        Text(title, size=14, color=Colors.GREY_600, no_wrap=False),
                        Text(value, size=24, weight=FontWeight.BOLD),
                        (
                            Text(subtitle, size=12, color=Colors.GREY_500)
                            if subtitle
                            else Container()
                        ),
                    ],
                    spacing=2,
                ),
            ],
            alignment=MainAxisAlignment.SPACE_BETWEEN,
        )

        return Container(
            content=card_content,
            padding=Padding.all(20),
            expand=1,
            height=120,
            on_click=on_click,
            ink=True if on_click else False,
            **CheckoutComponents.get_box_style(),
        )

    @staticmethod
    def create_action_button(
        text: str, icon: str, color: str, on_click, tooltip: str = None
    ) -> Control:
        """Create an action button"""
        return Container(
            content=Row(
                controls=[
                    Icon(icon, color=Colors.WHITE, size=20),
                    Text(text, color=Colors.WHITE, weight=FontWeight.BOLD, size=14),
                ],
                alignment=MainAxisAlignment.CENTER,
                spacing=10,
            ),
            bgcolor=color,
            padding=Padding.symmetric(horizontal=20, vertical=12),
            border_radius=BorderRadius.all(8),
            on_click=on_click,
            tooltip=tooltip,
            ink=True,
        )

    @staticmethod
    def create_transaction_item(
        date: str,
        description: str,
        amount: float,
        transaction_type: str,
        on_click=None,
    ) -> Control:
        """Create a transaction list item"""
        is_entry = transaction_type.lower() in ["entrée", "entry"]
        color = Colors.GREEN if is_entry else Colors.RED
        icon = Icons.ARROW_DOWNWARD if is_entry else Icons.ARROW_UPWARD

        return Container(
            content=Row(
                controls=[
                    Container(
                        content=Icon(icon, color=color, size=24),
                        bgcolor=f"{color}20",
                        padding=Padding.all(10),
                        border_radius=BorderRadius.all(8),
                    ),
                    Column(
                        controls=[
                            Text(description, weight=FontWeight.BOLD, size=14),
                            Text(date, size=12, color=Colors.GREY_600),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                    Text(
                        f"{'+' if is_entry else '-'}{amount:,.0f} $",
                        size=16,
                        weight=FontWeight.BOLD,
                        color=color,
                    ),
                ],
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=CrossAxisAlignment.CENTER,
            ),
            padding=Padding.all(15),
            border_radius=BorderRadius.all(8),
            border=Border.all(1, Colors.GREY_200),
            on_click=on_click,
            ink=True if on_click else False,
            margin=Margin.only(bottom=10),
        )

    @staticmethod
    def create_section_header(
        title: str, icon: str = None, action_button=None
    ) -> Control:
        """Create a section header"""
        controls = []

        if icon:
            controls.append(Icon(icon, color=Constants.PRIMARY_COLOR, size=24))

        controls.append(
            Text(
                title,
                size=20,
                weight=FontWeight.BOLD,
                color=Constants.PRIMARY_COLOR,
            )
        )

        header_row = Row(
            controls=controls,
            spacing=10,
        )

        if action_button:
            return Row(
                controls=[header_row, action_button],
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=CrossAxisAlignment.CENTER,
            )

        return header_row

    @staticmethod
    def create_empty_state(message: str, icon: str = Icons.INBOX) -> Control:
        """Create an empty state placeholder"""
        return Container(
            content=Column(
                controls=[
                    Icon(icon, size=80, color=Colors.GREY_300),
                    Text(
                        message,
                        size=16,
                        color=Colors.GREY_500,
                        text_align=TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            padding=Padding.all(40),
            alignment=Alignment.CENTER,
        )
