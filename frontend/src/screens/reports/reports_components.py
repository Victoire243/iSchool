"""
Reports Components Module
Contains reusable UI components for the reports screen
"""

from flet import *  # type: ignore
from core import Constants


class ReportsComponents:
    """Utility class for creating reports UI components"""

    @staticmethod
    def get_box_style() -> dict:
        """Return common box styling"""
        return {
            "border_radius": BorderRadius.all(10),
            "shadow": BoxShadow(color="black12", blur_radius=5, offset=Offset(0, 2)),
            "bgcolor": "#f8faff",
        }

    @staticmethod
    def create_section_header(
        title: str,
        icon: str = None,
        color: str = None,
    ) -> Control:
        """Create a section header"""
        if color is None:
            color = Constants.PRIMARY_COLOR

        controls = []
        if icon:
            controls.append(Icon(icon, color=color, size=24))

        controls.append(
            Text(
                title,
                size=18,
                weight=FontWeight.BOLD,
                color=color,
            )
        )

        return Container(
            content=Row(
                controls=controls,
                spacing=10,
                alignment=MainAxisAlignment.START,
            ),
            padding=Padding.symmetric(vertical=10),
        )

    @staticmethod
    def create_report_card(
        title: str,
        description: str,
        icon: str,
        color: str,
        on_generate,
        get_text_func,
    ) -> Control:
        """Create a report card button"""
        return Container(
            content=Column(
                controls=[
                    Icon(icon, color=color, size=48),
                    Text(
                        title,
                        size=16,
                        weight=FontWeight.BOLD,
                        text_align=TextAlign.CENTER,
                    ),
                    Text(
                        description,
                        size=12,
                        color=Colors.GREY_600,
                        text_align=TextAlign.CENTER,
                    ),
                    Container(height=10),
                    Button(
                        content=get_text_func("generate"),
                        icon=Icons.DOWNLOAD,
                        on_click=on_generate,
                        style=ButtonStyle(
                            shape=RoundedRectangleBorder(radius=5),
                            bgcolor=color,
                            padding=Padding(40, 20, 40, 20),
                            color="white",
                        ),
                    ),
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=5,
            ),
            padding=Padding.all(20),
            expand=1,
            height=250,
            **ReportsComponents.get_box_style(),
        )

    @staticmethod
    def create_export_button(
        text: str,
        icon: str,
        color: str,
        on_click,
        tooltip: str = None,
    ) -> Control:
        """Create an export button"""
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
    def create_filter_section(
        report_type_dropdown: Dropdown,
        period_dropdown: Dropdown,
        start_date_field: TextField,
        end_date_field: TextField,
        on_apply,
        on_reset,
        classroom_dropdown: Dropdown = None,
        student_dropdown: Dropdown = None,
        staff_dropdown: Dropdown = None,
        get_text_func=None,
    ) -> Control:
        """Create a filter section for reports"""
        filters = [
            report_type_dropdown,
            period_dropdown,
        ]

        # Add conditional filters
        if start_date_field and end_date_field:
            filters.extend(
                [
                    Row(
                        controls=[start_date_field, end_date_field],
                        spacing=10,
                    ),
                ]
            )

        if classroom_dropdown:
            filters.append(classroom_dropdown)

        if student_dropdown:
            filters.append(student_dropdown)

        if staff_dropdown:
            filters.append(staff_dropdown)

        # Add action buttons
        filters.append(
            Container(
                content=Row(
                    controls=[
                        Button(
                            content=(
                                get_text_func("apply_filters")
                                if get_text_func
                                else "Apply"
                            ),
                            icon=Icons.FILTER_ALT,
                            on_click=on_apply,
                            bgcolor=Constants.PRIMARY_COLOR,
                            color=Colors.WHITE,
                        ),
                        OutlinedButton(
                            content=(
                                get_text_func("reset_filters")
                                if get_text_func
                                else "Reset"
                            ),
                            icon=Icons.REFRESH,
                            on_click=on_reset,
                        ),
                    ],
                    spacing=10,
                ),
                padding=Padding.symmetric(vertical=10),
            )
        )

        return Container(
            content=Column(
                controls=filters,
                spacing=15,
            ),
            padding=Padding.all(20),
            **ReportsComponents.get_box_style(),
        )

    @staticmethod
    def create_preview_section(data_table: DataTable, get_text_func) -> Control:
        """Create a preview section for report data"""
        return Container(
            content=Column(
                controls=[
                    ReportsComponents.create_section_header(
                        title=get_text_func("preview"),
                        icon=Icons.PREVIEW,
                    ),
                    Container(
                        content=data_table,
                        border=border.all(1, Colors.GREY_300),
                        border_radius=BorderRadius.all(8),
                        padding=Padding.all(10),
                    ),
                ],
                spacing=10,
            ),
            padding=Padding.all(20),
            **ReportsComponents.get_box_style(),
        )

    @staticmethod
    def create_stats_summary(
        stats: dict,
        get_text_func,
    ) -> Control:
        """Create a statistics summary section"""
        stat_items = []
        for key, value in stats.items():
            stat_items.append(
                Row(
                    controls=[
                        Text(
                            get_text_func(key),
                            size=14,
                            weight=FontWeight.BOLD,
                        ),
                        Text(
                            str(value),
                            size=14,
                            color=Colors.GREY_700,
                        ),
                    ],
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                )
            )

        return Container(
            content=Column(
                controls=[
                    ReportsComponents.create_section_header(
                        title=get_text_func("summary"),
                        icon=Icons.ASSESSMENT,
                    ),
                    *stat_items,
                ],
                spacing=10,
            ),
            padding=Padding.all(20),
            **ReportsComponents.get_box_style(),
        )
