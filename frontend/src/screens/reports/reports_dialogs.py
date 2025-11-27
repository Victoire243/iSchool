"""
Reports Dialogs Module
Contains all dialog components for the reports screen
"""

from flet import *  # type: ignore
from core import Constants


class ReportsDialogs:
    """Manages all dialogs for the reports screen"""

    def __init__(self, screen):
        self.screen = screen

    def get_text(self, key: str) -> str:
        """Get translated text"""
        return self.screen.get_text(key)

    # ========================================================================
    # EXPORT DIALOGS
    # ========================================================================

    def show_export_options_dialog(self, report_type: str, report_data: list):
        """Show export options dialog"""

        def on_export_excel(e):
            self.close_dialog()
            self.screen.form_handlers.export_to_excel(report_type, report_data)

        def on_export_pdf(e):
            self.close_dialog()
            self.screen.form_handlers.export_to_pdf(report_type, report_data)

        def on_print(e):
            self.close_dialog()
            self.screen.form_handlers.print_report(report_type, report_data)

        def on_cancel(e):
            self.close_dialog()

        export_dialog = AlertDialog(
            modal=True,
            title=Text(self.get_text("export_options")),
            content=Column(
                controls=[
                    Text(self.get_text("choose_export_format")),
                    Container(height=10),
                    Button(
                        content=self.get_text("export_excel"),
                        icon=Icons.TABLE_CHART,
                        on_click=on_export_excel,
                        bgcolor=Colors.GREEN,
                        color=Colors.WHITE,
                        width=200,
                    ),
                    Button(
                        content=self.get_text("export_pdf"),
                        icon=Icons.PICTURE_AS_PDF,
                        on_click=on_export_pdf,
                        bgcolor=Colors.RED,
                        color=Colors.WHITE,
                        width=200,
                    ),
                    Button(
                        content=self.get_text("print"),
                        icon=Icons.PRINT,
                        on_click=on_print,
                        bgcolor=Constants.PRIMARY_COLOR,
                        color=Colors.WHITE,
                        width=200,
                    ),
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=10,
                tight=True,
            ),
            actions=[
                TextButton(
                    content=self.get_text("cancel"),
                    on_click=on_cancel,
                ),
            ],
            actions_alignment=MainAxisAlignment.END,
        )

        self.open_dialog(export_dialog)

    def show_success_dialog(self, message: str):
        """Show success dialog"""

        def on_close(e):
            self.close_dialog()

        success_dialog = AlertDialog(
            modal=True,
            title=Row(
                controls=[
                    Icon(Icons.CHECK_CIRCLE, color=Colors.GREEN, size=30),
                    Text(self.get_text("success")),
                ],
                spacing=10,
            ),
            content=Text(message),
            actions=[
                TextButton(
                    content=self.get_text("ok"),
                    on_click=on_close,
                ),
            ],
            actions_alignment=MainAxisAlignment.END,
        )

        self.open_dialog(success_dialog)

    def show_error_dialog(self, message: str):
        """Show error dialog"""

        def on_close(e):
            self.close_dialog()

        error_dialog = AlertDialog(
            modal=True,
            title=Row(
                controls=[
                    Icon(Icons.ERROR, color=Colors.RED, size=30),
                    Text(self.get_text("error")),
                ],
                spacing=10,
            ),
            content=Text(message),
            actions=[
                TextButton(
                    content=self.get_text("ok"),
                    on_click=on_close,
                ),
            ],
            actions_alignment=MainAxisAlignment.END,
        )

        self.open_dialog(error_dialog)

    def show_preview_dialog(self, report_type: str, report_data: list):
        """Show report preview dialog"""

        def on_close(e):
            self.close_dialog()

        def on_export(e):
            self.close_dialog()
            self.show_export_options_dialog(report_type, report_data)

        # Create a simple preview based on report type
        preview_content = Column(
            controls=[
                Text(
                    f"{self.get_text('preview')}: {report_type}",
                    size=16,
                    weight=FontWeight.BOLD,
                ),
                Container(height=10),
                Text(f"{self.get_text('total_records')}: {len(report_data)}"),
                Container(height=10),
                Container(
                    content=Text(self.get_text("preview_available_after_export")),
                    bgcolor=Colors.BLUE_50,
                    padding=Padding.all(10),
                    border_radius=BorderRadius.all(8),
                ),
            ],
            spacing=5,
            scroll=ScrollMode.AUTO,
            height=300,
        )

        preview_dialog = AlertDialog(
            modal=True,
            title=Text(self.get_text("report_preview")),
            content=preview_content,
            actions=[
                TextButton(
                    content=self.get_text("close"),
                    on_click=on_close,
                ),
                Button(
                    content=self.get_text("export"),
                    icon=Icons.DOWNLOAD,
                    on_click=on_export,
                    bgcolor=Constants.PRIMARY_COLOR,
                    color=Colors.WHITE,
                ),
            ],
            actions_alignment=MainAxisAlignment.SPACE_BETWEEN,
        )

        self.open_dialog(preview_dialog)

    def show_loading_dialog(self, message: str = None):
        """Show loading dialog"""
        if message is None:
            message = self.get_text("generating_report")

        loading_dialog = AlertDialog(
            modal=True,
            content=Row(
                controls=[
                    ProgressRing(),
                    Container(width=20),
                    Text(message),
                ],
                alignment=MainAxisAlignment.CENTER,
            ),
        )

        self.open_dialog(loading_dialog)
        return loading_dialog

    def close_loading_dialog(self, dialog: AlertDialog):
        """Close loading dialog"""
        self.close_dialog()

    def close_dialog(self):
        """Close current dialog"""
        try:
            self.screen.page.pop_dialog()
        except Exception:
            pass

    def open_dialog(self, dialog: AlertDialog):
        """Open a dialog"""
        self.screen.page.show_dialog(dialog=dialog)
