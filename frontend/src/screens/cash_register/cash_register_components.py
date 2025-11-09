"""
Cash Register Components Module
Contains reusable UI components for the cash register screen
"""

from flet import *  # type: ignore
from core import Constants


class CashRegisterComponents:
    """Utility class for creating cash register UI components"""

    @staticmethod
    def get_box_style() -> dict:
        """Return common box styling"""
        return {
            "border_radius": BorderRadius.all(10),
            "shadow": BoxShadow(color="black12", blur_radius=5, offset=Offset(0, 2)),
            "bgcolor": "#f8faff",
        }

    @staticmethod
    def create_stat_card(
        title: str, value: str, icon: str, color: str, subtitle: str = None
    ) -> Control:
        """Create a statistics card"""
        controls = [
            Text(title, size=14, color=Colors.GREY_600, no_wrap=False),
            Text(value, size=24, weight=FontWeight.BOLD, color=color),
        ]
        
        if subtitle:
            controls.append(
                Text(subtitle, size=12, color=Colors.GREY_500, italic=True)
            )
        
        return Container(
            content=Row(
                controls=[
                    Icon(icon, color=color, size=40),
                    Column(
                        controls=controls,
                        spacing=2,
                        alignment=MainAxisAlignment.CENTER,
                    ),
                ],
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=CrossAxisAlignment.CENTER,
            ),
            padding=Padding.all(20),
            expand=1,
            height=120,
            **CashRegisterComponents.get_box_style(),
        )

    @staticmethod
    def create_entry_type_badge(entry_type: str) -> Control:
        """Create a badge for entry type (Entrée/Sortie)"""
        if entry_type.lower() == "entrée":
            return Container(
                content=Text(
                    entry_type,
                    size=12,
                    weight=FontWeight.BOLD,
                    color=Colors.WHITE,
                ),
                bgcolor=Colors.GREEN,
                padding=Padding.symmetric(horizontal=10, vertical=5),
                border_radius=BorderRadius.all(5),
            )
        else:  # Sortie
            return Container(
                content=Text(
                    entry_type,
                    size=12,
                    weight=FontWeight.BOLD,
                    color=Colors.WHITE,
                ),
                bgcolor=Colors.RED,
                padding=Padding.symmetric(horizontal=10, vertical=5),
                border_radius=BorderRadius.all(5),
            )

    @staticmethod
    def create_filter_chip(label: str, selected: bool = False) -> Control:
        """Create a filter chip"""
        return Container(
            content=Text(
                label,
                size=14,
                weight=FontWeight.BOLD if selected else FontWeight.NORMAL,
                color=Colors.WHITE if selected else Constants.PRIMARY_COLOR,
            ),
            bgcolor=Constants.PRIMARY_COLOR if selected else Colors.TRANSPARENT,
            padding=Padding.symmetric(horizontal=15, vertical=8),
            border_radius=BorderRadius.all(20),
            border=Border.all(
                width=2,
                color=Constants.PRIMARY_COLOR,
            ),
        )

    @staticmethod
    def format_currency(amount: float) -> str:
        """Format amount as currency"""
        return f"{amount:,.2f} FC"

    @staticmethod
    def format_date(date_str: str) -> str:
        """Format date string for display"""
        try:
            from datetime import datetime
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            return date_obj.strftime("%d/%m/%Y")
        except:
            return date_str
