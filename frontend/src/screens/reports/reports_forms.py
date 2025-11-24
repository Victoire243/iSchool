"""
Reports Forms Module
Contains all form UI elements for the reports screen
"""

from flet import *  # type: ignore
from core import Constants
from datetime import datetime


class ReportsForms:
    """Manages all forms for the reports screen"""

    def __init__(self, screen):
        self.screen = screen

    def get_text(self, key: str) -> str:
        """Get translated text"""
        return self.screen.get_text(key)

    # ========================================================================
    # FILTER FORMS
    # ========================================================================

    def build_students_filter_form(self) -> Column:
        """Build filter form for students report"""
        self.students_classroom_dropdown = Dropdown(
            label=self.get_text("classroom"),
            hint_text=self.get_text("select_classroom"),
            options=[
                dropdown.Option(key="all", text=self.get_text("all_classrooms")),
            ],
            value="all",
            width=300,
        )

        # Populate classrooms
        for classroom in self.screen.classrooms_list:
            self.students_classroom_dropdown.options.append(
                dropdown.Option(
                    key=str(classroom.id_classroom),
                    text=classroom.name,
                )
            )

        return Column(
            controls=[
                Text(
                    self.get_text("students_report_filters"),
                    size=16,
                    weight=FontWeight.BOLD,
                ),
                self.students_classroom_dropdown,
            ],
            spacing=10,
        )

    def build_financial_filter_form(self, report_type: str = "school") -> Column:
        """Build filter form for financial reports"""
        controls = [
            Text(
                self.get_text("financial_report_filters"),
                size=16,
                weight=FontWeight.BOLD,
            ),
        ]

        # Period selection
        self.financial_period_dropdown = Dropdown(
            label=self.get_text("period"),
            hint_text=self.get_text("select_period"),
            options=[
                dropdown.Option(key="all", text=self.get_text("all_periods")),
                dropdown.Option(
                    key="current_month", text=self.get_text("current_month")
                ),
                dropdown.Option(key="last_month", text=self.get_text("last_month")),
                dropdown.Option(key="current_year", text=self.get_text("current_year")),
                dropdown.Option(key="custom", text=self.get_text("custom_period")),
            ],
            value="all",
            width=300,
            on_change=self.screen.on_period_change,
        )
        controls.append(self.financial_period_dropdown)

        # Date range (for custom period)
        self.financial_start_date = TextField(
            label=self.get_text("start_date"),
            hint_text="YYYY-MM-DD",
            width=200,
            visible=False,
        )
        self.financial_end_date = TextField(
            label=self.get_text("end_date"),
            hint_text="YYYY-MM-DD",
            width=200,
            visible=False,
        )
        controls.append(
            Row(
                controls=[
                    self.financial_start_date,
                    self.financial_end_date,
                ],
                spacing=10,
            )
        )

        # Type-specific filters
        if report_type == "classroom":
            self.financial_classroom_dropdown = Dropdown(
                label=self.get_text("classroom"),
                hint_text=self.get_text("select_classroom"),
                options=[
                    dropdown.Option(key="all", text=self.get_text("all_classrooms")),
                ],
                value="all",
                width=300,
            )
            # Populate classrooms
            for classroom in self.screen.classrooms_list:
                self.financial_classroom_dropdown.options.append(
                    dropdown.Option(
                        key=str(classroom.id_classroom),
                        text=classroom.name,
                    )
                )
            controls.append(self.financial_classroom_dropdown)

        elif report_type == "student":
            # Student search field with suggestions
            self.financial_student_search_field = TextField(
                label=self.get_text("search_student"),
                hint_text=self.get_text("enter_student_name"),
                on_change=self.screen.handle_financial_student_search_change,
                prefix_icon=Icons.SEARCH,
                suffix=IconButton(
                    icon=Icons.CLEAR,
                    tooltip=self.get_text("clear"),
                    on_click=self.screen.clear_financial_student_search,
                ),
                border_color=Constants.PRIMARY_COLOR,
                focused_border_color=Constants.PRIMARY_COLOR,
                width=400,
            )

            # Container for student suggestions
            self.financial_student_suggestions_container = Container(
                visible=False,
                width=400,
                height=250,
                bgcolor=Colors.WHITE,
                border=Border.all(1, Colors.GREY_300),
                border_radius=BorderRadius.all(5),
                padding=Padding.all(5),
            )

            # Selected student info display
            self.financial_student_info_text = Text(
                value="",
                size=14,
                color=Constants.PRIMARY_COLOR,
            )

            controls.append(
                Column(
                    controls=[
                        self.financial_student_search_field,
                        self.financial_student_suggestions_container,
                        self.financial_student_info_text,
                    ],
                    spacing=5,
                )
            )

        return Column(
            controls=controls,
            spacing=10,
        )

    def build_staff_payments_filter_form(self) -> Column:
        """Build filter form for staff payments report"""
        # Staff selection
        self.staff_payment_staff_dropdown = Dropdown(
            label=self.get_text("staff_member"),
            hint_text=self.get_text("select_staff"),
            options=[
                dropdown.Option(key="all", text=self.get_text("all_staff")),
            ],
            value="all",
            width=300,
        )

        # Populate staff
        for staff in self.screen.staff_list:
            self.staff_payment_staff_dropdown.options.append(
                dropdown.Option(
                    key=str(staff.id_staff),
                    text=f"{staff.first_name} {staff.last_name}",
                )
            )

        # Period selection
        self.staff_payment_period_dropdown = Dropdown(
            label=self.get_text("period"),
            hint_text=self.get_text("select_period"),
            options=[
                dropdown.Option(key="all", text=self.get_text("all_periods")),
                dropdown.Option(
                    key="current_month", text=self.get_text("current_month")
                ),
                dropdown.Option(key="last_month", text=self.get_text("last_month")),
                dropdown.Option(key="current_year", text=self.get_text("current_year")),
                dropdown.Option(key="custom", text=self.get_text("custom_period")),
            ],
            value="all",
            width=300,
            on_change=self.screen.on_staff_payment_period_change,
        )

        # Date range (for custom period)
        self.staff_payment_start_date = TextField(
            label=self.get_text("start_date"),
            hint_text="YYYY-MM-DD",
            width=200,
            visible=False,
        )
        self.staff_payment_end_date = TextField(
            label=self.get_text("end_date"),
            hint_text="YYYY-MM-DD",
            width=200,
            visible=False,
        )

        return Column(
            controls=[
                Text(
                    self.get_text("staff_payments_report_filters"),
                    size=16,
                    weight=FontWeight.BOLD,
                ),
                self.staff_payment_staff_dropdown,
                self.staff_payment_period_dropdown,
                Row(
                    controls=[
                        self.staff_payment_start_date,
                        self.staff_payment_end_date,
                    ],
                    spacing=10,
                ),
            ],
            spacing=10,
        )

    def build_cash_register_filter_form(self) -> Column:
        """Build filter form for cash register report"""
        # Period selection
        self.cash_register_period_dropdown = Dropdown(
            label=self.get_text("period"),
            hint_text=self.get_text("select_period"),
            options=[
                dropdown.Option(key="all", text=self.get_text("all_periods")),
                dropdown.Option(
                    key="current_month", text=self.get_text("current_month")
                ),
                dropdown.Option(key="last_month", text=self.get_text("last_month")),
                dropdown.Option(key="current_year", text=self.get_text("current_year")),
                dropdown.Option(key="custom", text=self.get_text("custom_period")),
            ],
            value="all",
            width=300,
            on_change=self.screen.on_cash_register_period_change,
        )

        # Date range (for custom period)
        self.cash_register_start_date = TextField(
            label=self.get_text("start_date"),
            hint_text="YYYY-MM-DD",
            width=200,
            visible=False,
        )
        self.cash_register_end_date = TextField(
            label=self.get_text("end_date"),
            hint_text="YYYY-MM-DD",
            width=200,
            visible=False,
        )

        return Column(
            controls=[
                Text(
                    self.get_text("cash_register_report_filters"),
                    size=16,
                    weight=FontWeight.BOLD,
                ),
                self.cash_register_period_dropdown,
                Row(
                    controls=[
                        self.cash_register_start_date,
                        self.cash_register_end_date,
                    ],
                    spacing=10,
                ),
            ],
            spacing=10,
        )
