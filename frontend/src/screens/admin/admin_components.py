"""
Admin Components Module
Contains reusable UI components for the admin screen
"""

from flet import *  # type: ignore
from core import Constants


class AdminComponents:
    """Utility class for creating admin UI components"""

    @staticmethod
    def get_box_style() -> dict:
        """Return common box styling"""
        return {
            "border_radius": BorderRadius.all(10),
            "shadow": BoxShadow(color="black12", blur_radius=5, offset=Offset(0, 2)),
            "bgcolor": "#f8faff",
        }

    @staticmethod
    def get_color_by_user_role(role: str) -> ColorValue:
        """Get color based on user role"""
        if not role.strip():
            return Colors.GREEN
        match role.lower()[0]:
            case "a":  # Admin
                return Colors.RED
            case "c":  # Comptable
                return Colors.ORANGE
            case "e":  # Enseignant
                return Constants.PRIMARY_COLOR
            case "s":  # Surveillant
                return Constants.SECONDARY_COLOR
        return Colors.ORANGE

    @staticmethod
    def create_stat_card(
        title: str, value: str, icon: str, color: str, subtitle: str = None
    ) -> Control:
        """Create a statistics card"""
        return Container(
            content=Row(
                controls=[
                    Icon(icon, color=color, size=30),
                    Column(
                        controls=[
                            Text(title, size=14, color=Colors.GREY_600, no_wrap=False),
                            Text(value, size=20, weight=FontWeight.BOLD),
                        ],
                        spacing=0,
                    ),
                ],
                alignment=MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=Padding.all(15),
            expand=1,
            height=100,
            **AdminComponents.get_box_style(),
        )
