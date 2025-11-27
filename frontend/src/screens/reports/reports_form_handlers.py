"""
Reports Form Handlers Module
Handles form submission logic and export operations for the reports screen
"""

import asyncio
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import json


class ReportsFormHandlers:
    """Manages form submission and business logic for reports"""

    def __init__(self, screen):
        self.screen = screen

    def get_text(self, key: str) -> str:
        """Get translated text"""
        return self.screen.get_text(key)

    # ========================================================================
    # DATE RANGE HELPERS
    # ========================================================================

    def get_date_range(self, period: str) -> tuple[Optional[str], Optional[str]]:
        """Get start and end dates based on period selection"""
        today = datetime.now()

        if period == "all":
            return (None, None)
        elif period == "current_month":
            start_date = today.replace(day=1).strftime("%Y-%m-%d")
            end_date = today.strftime("%Y-%m-%d")
            return (start_date, end_date)
        elif period == "last_month":
            first_day_this_month = today.replace(day=1)
            last_day_last_month = first_day_this_month - timedelta(days=1)
            first_day_last_month = last_day_last_month.replace(day=1)
            return (
                first_day_last_month.strftime("%Y-%m-%d"),
                last_day_last_month.strftime("%Y-%m-%d"),
            )
        elif period == "current_year":
            start_date = today.replace(month=1, day=1).strftime("%Y-%m-%d")
            end_date = today.strftime("%Y-%m-%d")
            return (start_date, end_date)
        else:
            return (None, None)

    # ========================================================================
    # REPORT GENERATION HANDLERS
    # ========================================================================

    async def handle_generate_students_report(self):
        """Handle students report generation"""
        try:
            # Get filter values
            classroom_id = None
            if hasattr(self.screen.forms, "students_classroom_dropdown"):
                classroom_value = self.screen.forms.students_classroom_dropdown.value
                if classroom_value and classroom_value != "all":
                    classroom_id = int(classroom_value)

            # Show loading
            loading_dialog = self.screen.dialogs.show_loading_dialog(
                self.get_text("generating_report")
            )

            # Generate report
            success, report_data = await self.screen.services.generate_students_report(
                classroom_id=classroom_id
            )

            # Close loading
            self.screen.dialogs.close_loading_dialog(loading_dialog)

            if success and report_data:
                # Update preview
                self.screen.current_report_data = report_data
                self.screen.current_report_type = "students"
                self.update_preview_section("students", report_data)

                # Show export options
                self.screen.dialogs.show_export_options_dialog("students", report_data)
            else:
                self.screen.dialogs.show_error_dialog(self.get_text("no_data_found"))

        except Exception as e:
            print(f"Error generating students report: {e}")
            self.screen.dialogs.show_error_dialog(str(e))

    async def handle_generate_staff_payments_report(self):
        """Handle staff payments report generation"""
        try:
            # Get filter values
            staff_id = None
            if hasattr(self.screen.forms, "staff_payment_staff_dropdown"):
                staff_value = self.screen.forms.staff_payment_staff_dropdown.value
                if staff_value and staff_value != "all":
                    staff_id = int(staff_value)

            # Get date range
            start_date, end_date = None, None
            if hasattr(self.screen.forms, "staff_payment_period_dropdown"):
                period = self.screen.forms.staff_payment_period_dropdown.value
                if period == "custom":
                    start_date = self.screen.forms.staff_payment_start_date.value
                    end_date = self.screen.forms.staff_payment_end_date.value
                else:
                    start_date, end_date = self.get_date_range(period)

            # Show loading
            loading_dialog = self.screen.dialogs.show_loading_dialog()

            # Generate report
            success, report_data = (
                await self.screen.services.generate_staff_payments_report(
                    staff_id=staff_id,
                    start_date=start_date,
                    end_date=end_date,
                )
            )

            # Close loading
            self.screen.dialogs.close_loading_dialog(loading_dialog)

            if success and report_data:
                self.screen.current_report_data = report_data
                self.screen.current_report_type = "staff_payments"
                self.update_preview_section("staff_payments", report_data)
                self.screen.dialogs.show_export_options_dialog(
                    "staff_payments", report_data
                )
            else:
                self.screen.dialogs.show_error_dialog(self.get_text("no_data_found"))

        except Exception as e:
            print(f"Error generating staff payments report: {e}")
            self.screen.dialogs.show_error_dialog(str(e))

    async def handle_generate_financial_classroom_report(self):
        """Handle financial report by classroom generation"""
        try:
            # Get filter values
            classroom_id = None
            if hasattr(self.screen.forms, "financial_classroom_dropdown"):
                classroom_value = self.screen.forms.financial_classroom_dropdown.value
                if classroom_value and classroom_value != "all":
                    classroom_id = int(classroom_value)

            # Get date range
            start_date, end_date = None, None
            if hasattr(self.screen.forms, "financial_period_dropdown"):
                period = self.screen.forms.financial_period_dropdown.value
                if period == "custom":
                    start_date = self.screen.forms.financial_start_date.value
                    end_date = self.screen.forms.financial_end_date.value
                else:
                    start_date, end_date = self.get_date_range(period)

            # Show loading
            loading_dialog = self.screen.dialogs.show_loading_dialog()

            # Generate report
            success, report_result = (
                await self.screen.services.generate_financial_report_by_classroom(
                    classroom_id=classroom_id,
                    start_date=start_date,
                    end_date=end_date,
                )
            )

            # Close loading
            self.screen.dialogs.close_loading_dialog(loading_dialog)

            if success and report_result:
                report_data = report_result.get("classrooms", [])
                self.screen.current_report_data = report_data
                self.screen.current_report_type = "financial_classroom"
                self.screen.current_report_summary = {
                    "total": report_result.get("total", 0)
                }
                self.update_preview_section("financial_classroom", report_data)
                self.screen.dialogs.show_export_options_dialog(
                    "financial_classroom", report_data
                )
            else:
                self.screen.dialogs.show_error_dialog(self.get_text("no_data_found"))

        except Exception as e:
            print(f"Error generating financial classroom report: {e}")
            self.screen.dialogs.show_error_dialog(str(e))

    async def handle_generate_financial_student_report(self):
        """Handle financial report by student generation"""
        try:
            # Get filter values - use the selected student from search
            student_id = self.screen.selected_financial_student_id

            # Get date range
            start_date, end_date = None, None
            if hasattr(self.screen.forms, "financial_period_dropdown"):
                period = self.screen.forms.financial_period_dropdown.value
                if period == "custom":
                    start_date = self.screen.forms.financial_start_date.value
                    end_date = self.screen.forms.financial_end_date.value
                else:
                    start_date, end_date = self.get_date_range(period)

            # Show loading
            loading_dialog = self.screen.dialogs.show_loading_dialog()

            # Generate report
            success, report_data = (
                await self.screen.services.generate_financial_report_by_student(
                    student_id=student_id,
                    start_date=start_date,
                    end_date=end_date,
                )
            )

            # Close loading
            self.screen.dialogs.close_loading_dialog(loading_dialog)

            if success and report_data:
                self.screen.current_report_data = report_data
                self.screen.current_report_type = "financial_student"
                self.update_preview_section("financial_student", report_data)
                self.screen.dialogs.show_export_options_dialog(
                    "financial_student", report_data
                )
            else:
                self.screen.dialogs.show_error_dialog(self.get_text("no_data_found"))

        except Exception as e:
            print(f"Error generating financial student report: {e}")
            self.screen.dialogs.show_error_dialog(str(e))

    async def handle_generate_school_financial_report(self):
        """Handle overall school financial report generation"""
        try:
            # Get date range
            start_date, end_date = None, None
            if hasattr(self.screen.forms, "financial_period_dropdown"):
                period = self.screen.forms.financial_period_dropdown.value
                if period == "custom":
                    start_date = self.screen.forms.financial_start_date.value
                    end_date = self.screen.forms.financial_end_date.value
                else:
                    start_date, end_date = self.get_date_range(period)

            # Show loading
            loading_dialog = self.screen.dialogs.show_loading_dialog()

            # Generate report
            success, report_data = (
                await self.screen.services.generate_school_financial_report(
                    start_date=start_date,
                    end_date=end_date,
                )
            )

            # Close loading
            self.screen.dialogs.close_loading_dialog(loading_dialog)

            if success and report_data:
                # Convert to list format for export
                report_list = [report_data]
                self.screen.current_report_data = report_list
                self.screen.current_report_type = "financial_school"
                self.screen.current_report_summary = report_data
                self.update_preview_section("financial_school", report_list)
                self.screen.dialogs.show_export_options_dialog(
                    "financial_school", report_list
                )
            else:
                self.screen.dialogs.show_error_dialog(self.get_text("no_data_found"))

        except Exception as e:
            print(f"Error generating school financial report: {e}")
            self.screen.dialogs.show_error_dialog(str(e))

    async def handle_generate_cash_register_report(self):
        """Handle cash register report generation"""
        try:
            # Get date range
            start_date, end_date = None, None
            if hasattr(self.screen.forms, "cash_register_period_dropdown"):
                period = self.screen.forms.cash_register_period_dropdown.value
                if period == "custom":
                    start_date = self.screen.forms.cash_register_start_date.value
                    end_date = self.screen.forms.cash_register_end_date.value
                else:
                    start_date, end_date = self.get_date_range(period)

            # Show loading
            loading_dialog = self.screen.dialogs.show_loading_dialog()

            # Generate report
            success, report_data = (
                await self.screen.services.generate_cash_register_report(
                    start_date=start_date,
                    end_date=end_date,
                )
            )

            # Close loading
            self.screen.dialogs.close_loading_dialog(loading_dialog)

            if success and report_data:
                self.screen.current_report_data = report_data
                self.screen.current_report_type = "cash_register"
                self.update_preview_section("cash_register", report_data)
                self.screen.dialogs.show_export_options_dialog(
                    "cash_register", report_data
                )
            else:
                self.screen.dialogs.show_error_dialog(self.get_text("no_data_found"))

        except Exception as e:
            print(f"Error generating cash register report: {e}")
            self.screen.dialogs.show_error_dialog(str(e))

    async def handle_generate_users_report(self):
        """Handle users report generation"""
        try:
            # Show loading
            loading_dialog = self.screen.dialogs.show_loading_dialog()

            # Generate report
            success, report_data = await self.screen.services.generate_users_report()

            # Close loading
            self.screen.dialogs.close_loading_dialog(loading_dialog)

            if success and report_data:
                self.screen.current_report_data = report_data
                self.screen.current_report_type = "users"
                self.update_preview_section("users", report_data)
                self.screen.dialogs.show_export_options_dialog("users", report_data)
            else:
                self.screen.dialogs.show_error_dialog(self.get_text("no_data_found"))

        except Exception as e:
            print(f"Error generating users report: {e}")
            self.screen.dialogs.show_error_dialog(str(e))

    # ========================================================================
    # PREVIEW UPDATE
    # ========================================================================

    def update_preview_section(self, report_type: str, data: List[Dict[str, Any]]):
        """Update the preview section with report data"""
        try:
            # Build appropriate preview table based on report type
            if report_type == "students":
                preview_table = self.screen.tables.build_students_preview_table(data)
            elif report_type == "staff_payments":
                preview_table = self.screen.tables.build_staff_payments_preview_table(
                    data
                )
            elif report_type == "financial_classroom":
                preview_table = (
                    self.screen.tables.build_financial_classroom_preview_table(data)
                )
            elif report_type == "financial_student":
                preview_table = (
                    self.screen.tables.build_financial_student_preview_table(data)
                )
            elif report_type == "cash_register":
                preview_table = self.screen.tables.build_cash_register_preview_table(
                    data
                )
            elif report_type == "users":
                preview_table = self.screen.tables.build_users_preview_table(data)
            else:
                return

            # Update preview in the UI
            if hasattr(self.screen, "preview_container"):
                from flet import Column, Container, Text, ScrollMode
                from .reports_components import ReportsComponents

                self.screen.preview_container.content = Column(
                    controls=[
                        ReportsComponents.create_section_header(
                            title=self.get_text("preview"),
                            icon="preview",
                        ),
                        Container(
                            content=preview_table,
                            padding=10,
                        ),
                        Text(
                            f"{self.get_text('showing')} {min(10, len(data))} {self.get_text('of')} {len(data)} {self.get_text('records')}",
                            size=12,
                            italic=True,
                        ),
                    ],
                    scroll=ScrollMode.AUTO,
                )
                self.screen.preview_container.visible = True
                self.screen.preview_container.update()

        except Exception as e:
            print(f"Error updating preview section: {e}")

    # ========================================================================
    # EXPORT HANDLERS
    # ========================================================================

    def export_to_excel(self, report_type: str, data: List[Dict[str, Any]]):
        """Export report to Excel format"""
        try:
            # TODO: Implement actual Excel export using openpyxl or xlsxwriter
            # For now, save as JSON
            filename = (
                f"{report_type}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            self.screen.dialogs.show_success_dialog(
                f"{self.get_text('report_exported_successfully')}\n{filename}"
            )
        except Exception as e:
            print(f"Error exporting to Excel: {e}")
            self.screen.dialogs.show_error_dialog(str(e))

    def export_to_pdf(self, report_type: str, data: List[Dict[str, Any]]):
        """Export report to PDF format"""
        try:
            # TODO: Implement actual PDF export using reportlab or similar
            # For now, save as JSON
            filename = (
                f"{report_type}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            self.screen.dialogs.show_success_dialog(
                f"{self.get_text('report_exported_successfully')}\n{filename}"
            )
        except Exception as e:
            print(f"Error exporting to PDF: {e}")
            self.screen.dialogs.show_error_dialog(str(e))

    def print_report(self, report_type: str, data: List[Dict[str, Any]]):
        """Print report"""
        try:
            # TODO: Implement actual print functionality
            self.screen.dialogs.show_success_dialog(
                self.get_text("print_dialog_opened")
            )
        except Exception as e:
            print(f"Error printing report: {e}")
            self.screen.dialogs.show_error_dialog(str(e))
