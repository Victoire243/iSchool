"""
Reports Tables Module
Manages all table/list views for the reports screen
"""

from flet import *  # type: ignore
from core import Constants
from typing import List, Dict, Any


class ReportsTables:
    """Manages all tables and data displays for the reports screen"""

    def __init__(self, screen):
        self.screen = screen

    def get_text(self, key: str) -> str:
        """Get translated text"""
        return self.screen.get_text(key)

    # ========================================================================
    # PREVIEW TABLES
    # ========================================================================

    def build_students_preview_table(self, data: List[Dict[str, Any]]) -> DataTable:
        """Build preview table for students report"""
        columns = [
            DataColumn(Text(self.get_text("id"), weight=FontWeight.BOLD)),
            DataColumn(Text(self.get_text("first_name"), weight=FontWeight.BOLD)),
            DataColumn(Text(self.get_text("last_name"), weight=FontWeight.BOLD)),
            DataColumn(Text(self.get_text("gender"), weight=FontWeight.BOLD)),
            DataColumn(Text(self.get_text("date_of_birth"), weight=FontWeight.BOLD)),
            DataColumn(Text(self.get_text("classroom"), weight=FontWeight.BOLD)),
        ]

        rows = []
        for item in data[:10]:  # Show first 10 for preview
            rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(str(item.get("id", "")))),
                        DataCell(Text(item.get("first_name", ""))),
                        DataCell(Text(item.get("last_name", ""))),
                        DataCell(Text(item.get("gender", ""))),
                        DataCell(Text(item.get("date_of_birth", ""))),
                        DataCell(Text(item.get("classroom", ""))),
                    ]
                )
            )

        return DataTable(
            columns=columns,
            rows=rows,
            border=border.all(1, Colors.GREY_300),
            border_radius=BorderRadius.all(8),
            vertical_lines=border.BorderSide(1, Colors.GREY_300),
            horizontal_lines=border.BorderSide(1, Colors.GREY_300),
            heading_row_color=Colors.BLUE_50,
            heading_row_height=50,
            data_row_min_height=40,
            data_row_max_height=60,
        )

    def build_staff_payments_preview_table(
        self, data: List[Dict[str, Any]]
    ) -> DataTable:
        """Build preview table for staff payments report"""
        columns = [
            DataColumn(Text(self.get_text("id"), weight=FontWeight.BOLD)),
            DataColumn(Text(self.get_text("staff_name"), weight=FontWeight.BOLD)),
            DataColumn(Text(self.get_text("payment_date"), weight=FontWeight.BOLD)),
            DataColumn(Text(self.get_text("amount"), weight=FontWeight.BOLD)),
            DataColumn(Text(self.get_text("payment_type"), weight=FontWeight.BOLD)),
        ]

        rows = []
        for item in data[:10]:
            rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(str(item.get("id", "")))),
                        DataCell(Text(item.get("staff_name", ""))),
                        DataCell(Text(item.get("payment_date", ""))),
                        DataCell(Text(f"${item.get('amount', 0):.2f}")),
                        DataCell(Text(item.get("payment_type", ""))),
                    ]
                )
            )

        return DataTable(
            columns=columns,
            rows=rows,
            border=border.all(1, Colors.GREY_300),
            border_radius=BorderRadius.all(8),
            vertical_lines=border.BorderSide(1, Colors.GREY_300),
            horizontal_lines=border.BorderSide(1, Colors.GREY_300),
            heading_row_color=Colors.BLUE_50,
            heading_row_height=50,
            data_row_min_height=40,
            data_row_max_height=60,
        )

    def build_financial_classroom_preview_table(
        self, data: List[Dict[str, Any]]
    ) -> DataTable:
        """Build preview table for financial report by classroom"""
        columns = [
            DataColumn(Text(self.get_text("classroom"), weight=FontWeight.BOLD)),
            DataColumn(Text(self.get_text("total_amount"), weight=FontWeight.BOLD)),
            DataColumn(Text(self.get_text("payment_count"), weight=FontWeight.BOLD)),
            DataColumn(Text(self.get_text("student_count"), weight=FontWeight.BOLD)),
        ]

        rows = []
        for item in data:
            rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(item.get("classroom", ""))),
                        DataCell(Text(f"${item.get('total_amount', 0):.2f}")),
                        DataCell(Text(str(item.get("payment_count", 0)))),
                        DataCell(Text(str(item.get("student_count", 0)))),
                    ]
                )
            )

        return DataTable(
            columns=columns,
            rows=rows,
            border=border.all(1, Colors.GREY_300),
            border_radius=BorderRadius.all(8),
            vertical_lines=border.BorderSide(1, Colors.GREY_300),
            horizontal_lines=border.BorderSide(1, Colors.GREY_300),
            heading_row_color=Colors.BLUE_50,
            heading_row_height=50,
            data_row_min_height=40,
            data_row_max_height=60,
        )

    def build_financial_student_preview_table(
        self, data: List[Dict[str, Any]]
    ) -> DataTable:
        """Build preview table for financial report by student"""
        columns = [
            DataColumn(Text(self.get_text("student_id"), weight=FontWeight.BOLD)),
            DataColumn(Text(self.get_text("student_name"), weight=FontWeight.BOLD)),
            DataColumn(Text(self.get_text("total_amount"), weight=FontWeight.BOLD)),
            DataColumn(Text(self.get_text("payment_count"), weight=FontWeight.BOLD)),
        ]

        rows = []
        for item in data[:10]:
            rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(str(item.get("student_id", "")))),
                        DataCell(Text(item.get("student_name", ""))),
                        DataCell(Text(f"${item.get('total_amount', 0):.2f}")),
                        DataCell(Text(str(item.get("payment_count", 0)))),
                    ]
                )
            )

        return DataTable(
            columns=columns,
            rows=rows,
            border=border.all(1, Colors.GREY_300),
            border_radius=BorderRadius.all(8),
            vertical_lines=border.BorderSide(1, Colors.GREY_300),
            horizontal_lines=border.BorderSide(1, Colors.GREY_300),
            heading_row_color=Colors.BLUE_50,
            heading_row_height=50,
            data_row_min_height=40,
            data_row_max_height=60,
        )

    def build_cash_register_preview_table(
        self, data: List[Dict[str, Any]]
    ) -> DataTable:
        """Build preview table for cash register report"""
        columns = [
            DataColumn(Text(self.get_text("id"), weight=FontWeight.BOLD)),
            DataColumn(Text(self.get_text("date"), weight=FontWeight.BOLD)),
            DataColumn(Text(self.get_text("type"), weight=FontWeight.BOLD)),
            DataColumn(Text(self.get_text("description"), weight=FontWeight.BOLD)),
            DataColumn(Text(self.get_text("amount"), weight=FontWeight.BOLD)),
        ]

        rows = []
        for item in data[:10]:
            rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(str(item.get("id", "")))),
                        DataCell(Text(item.get("date", ""))),
                        DataCell(Text(item.get("type", ""))),
                        DataCell(Text(item.get("description", ""))),
                        DataCell(Text(f"${item.get('amount', 0):.2f}")),
                    ]
                )
            )

        return DataTable(
            columns=columns,
            rows=rows,
            border=border.all(1, Colors.GREY_300),
            border_radius=BorderRadius.all(8),
            vertical_lines=border.BorderSide(1, Colors.GREY_300),
            horizontal_lines=border.BorderSide(1, Colors.GREY_300),
            heading_row_color=Colors.BLUE_50,
            heading_row_height=50,
            data_row_min_height=40,
            data_row_max_height=60,
        )

    def build_users_preview_table(self, data: List[Dict[str, Any]]) -> DataTable:
        """Build preview table for users report"""
        columns = [
            DataColumn(Text(self.get_text("id"), weight=FontWeight.BOLD)),
            DataColumn(Text(self.get_text("username"), weight=FontWeight.BOLD)),
            DataColumn(Text(self.get_text("role_id"), weight=FontWeight.BOLD)),
            DataColumn(Text(self.get_text("is_active"), weight=FontWeight.BOLD)),
        ]

        rows = []
        for item in data[:10]:
            rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(str(item.get("id", "")))),
                        DataCell(Text(item.get("username", ""))),
                        DataCell(Text(str(item.get("role_id", "")))),
                        DataCell(Text(item.get("is_active", ""))),
                    ]
                )
            )

        return DataTable(
            columns=columns,
            rows=rows,
            border=border.all(1, Colors.GREY_300),
            border_radius=BorderRadius.all(8),
            vertical_lines=border.BorderSide(1, Colors.GREY_300),
            horizontal_lines=border.BorderSide(1, Colors.GREY_300),
            heading_row_color=Colors.BLUE_50,
            heading_row_height=50,
            data_row_min_height=40,
            data_row_max_height=60,
        )

    # ========================================================================
    # REPORT CARDS GRID
    # ========================================================================

    def build_report_cards_grid(self) -> Column:
        """Build grid of report cards"""
        from .reports_components import ReportsComponents

        # Students Reports Row
        students_row = Row(
            controls=[
                ReportsComponents.create_report_card(
                    title=self.get_text("students_list"),
                    description=self.get_text("export_all_students_or_by_class"),
                    icon=Icons.PEOPLE,
                    color=Colors.BLUE,
                    on_generate=lambda e: self.screen.show_report_section("students"),
                    get_text_func=self.get_text,
                ),
                ReportsComponents.create_report_card(
                    title=self.get_text("financial_by_student"),
                    description=self.get_text("student_payment_report"),
                    icon=Icons.ATTACH_MONEY,
                    color=Colors.GREEN,
                    on_generate=lambda e: self.screen.show_report_section(
                        "financial_student"
                    ),
                    get_text_func=self.get_text,
                ),
            ],
            spacing=15,
        )

        # Financial Reports Row
        financial_row = Row(
            controls=[
                ReportsComponents.create_report_card(
                    title=self.get_text("financial_by_classroom"),
                    description=self.get_text("classroom_payment_report"),
                    icon=Icons.CLASS_,
                    color=Colors.ORANGE,
                    on_generate=lambda e: self.screen.show_report_section(
                        "financial_classroom"
                    ),
                    get_text_func=self.get_text,
                ),
                ReportsComponents.create_report_card(
                    title=self.get_text("school_financial"),
                    description=self.get_text("overall_school_finances"),
                    icon=Icons.ACCOUNT_BALANCE,
                    color=Colors.PURPLE,
                    on_generate=lambda e: self.screen.show_report_section(
                        "financial_school"
                    ),
                    get_text_func=self.get_text,
                ),
            ],
            spacing=15,
        )

        # Staff and Operations Row
        operations_row = Row(
            controls=[
                ReportsComponents.create_report_card(
                    title=self.get_text("staff_payments"),
                    description=self.get_text("staff_payment_report"),
                    icon=Icons.PAYMENTS,
                    color=Colors.TEAL,
                    on_generate=lambda e: self.screen.show_report_section(
                        "staff_payments"
                    ),
                    get_text_func=self.get_text,
                ),
                ReportsComponents.create_report_card(
                    title=self.get_text("cash_register"),
                    description=self.get_text("cash_register_report"),
                    icon=Icons.POINT_OF_SALE,
                    color=Colors.AMBER,
                    on_generate=lambda e: self.screen.show_report_section(
                        "cash_register"
                    ),
                    get_text_func=self.get_text,
                ),
            ],
            spacing=15,
        )

        # System Row
        system_row = Row(
            controls=[
                ReportsComponents.create_report_card(
                    title=self.get_text("users_report"),
                    description=self.get_text("export_users_list"),
                    icon=Icons.SUPERVISED_USER_CIRCLE,
                    color=Colors.INDIGO,
                    on_generate=lambda e: self.screen.show_report_section("users"),
                    get_text_func=self.get_text,
                ),
            ],
            spacing=15,
        )

        return Column(
            controls=[
                students_row,
                Container(height=15),
                financial_row,
                Container(height=15),
                operations_row,
                Container(height=15),
                system_row,
            ],
            spacing=0,
        )
