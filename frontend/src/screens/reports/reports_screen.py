"""
Reports Screen - Modular Version
==================================
Page de gestion des rapports avec architecture modulaire.

Modules utilisés:
- reports_services.py : Gestion des appels API et logique métier
- reports_components.py : Composants UI réutilisables
- reports_forms.py : Gestion des formulaires
- reports_form_handlers.py : Logique de soumission des formulaires
- reports_tables.py : Gestion des tables et listes
- reports_dialogs.py : Gestion des dialogues
"""

from flet import *  # type: ignore
from core import AppState, Constants
import asyncio

from .reports_services import ReportsServices
from .reports_components import ReportsComponents
from .reports_forms import ReportsForms
from .reports_form_handlers import ReportsFormHandlers
from .reports_tables import ReportsTables
from .reports_dialogs import ReportsDialogs


class ReportsScreen:
    """
    Écran de gestion des rapports (Version modulaire).
    Permet de générer, visualiser et exporter divers rapports.
    """

    def __init__(self, app_state: AppState, page: Page | None = None) -> None:
        self.app_state = app_state
        self.page = page
        self.services = ReportsServices(self.app_state)

        # Initialize data structures
        self.students_list = []
        self.staff_list = []
        self.classrooms_list = []
        self.enrollments_list = []
        self.current_report_data = []
        self.current_report_type = None
        self.current_report_summary = {}

        # Current section
        self.current_section = "home"
        self.selected_financial_student_id = None

        # Initialize modules
        self.forms = ReportsForms(self)
        self.form_handlers = ReportsFormHandlers(self)
        self.tables = ReportsTables(self)
        self.dialogs = ReportsDialogs(self)

        # Build UI components
        self.build_components()

    # ========================================================================
    # LIFECYCLE METHODS
    # ========================================================================

    async def on_mount(self):
        """Called when the screen is mounted"""
        await self.load_initial_data()

    def refresh_reports_data(self, e):
        """Refresh all reports data"""
        self.main_content.content = self.loading_indicator
        self.main_content.update()
        asyncio.create_task(self.load_initial_data())

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def get_text(self, key: str) -> str:
        """Get translated text for a given key"""
        return self.app_state.translations.get(key, key)

    @staticmethod
    def get_box_style() -> dict:
        """Return common box styling"""
        return ReportsComponents.get_box_style()

    # ========================================================================
    # DATA LOADING
    # ========================================================================

    async def load_initial_data(self):
        """Load all necessary data for the reports screen"""
        try:
            # Load data in parallel
            (
                (students_status, students_data),
                (staff_status, staff_data),
                (classrooms_status, classrooms_data),
                (enrollments_status, enrollments_data),
            ) = await asyncio.gather(
                self.services.load_students_list(),
                self.services.load_staff_list(),
                self.services.load_classrooms_list(),
                self.services.load_enrollments_list(),
                return_exceptions=True,
            )

            # Store data
            self.students_list = students_data if students_status else []
            self.staff_list = staff_data if staff_status else []
            self.classrooms_list = classrooms_data if classrooms_status else []
            self.enrollments_list = enrollments_data if enrollments_status else []

            # Update main content to show report cards
            self.show_home_section()

            try:
                self.main_content.update()
            except Exception as e:
                print(f"Erreur lors de la mise à jour de l'interface: {e}")

        except Exception as e:
            print(f"Erreur lors du chargement des données: {e}")
            self.main_content.content = Text(f"Erreur: {e}")
            if hasattr(self.main_content, "update"):
                self.main_content.update()

    # ========================================================================
    # SECTION NAVIGATION
    # ========================================================================

    def show_home_section(self):
        """Show home section with report cards"""
        self.current_section = "home"

        # Build report cards grid
        report_cards = self.tables.build_report_cards_grid()

        self.main_content.content = Column(
            expand=True,
            horizontal_alignment=CrossAxisAlignment.STRETCH,
            scroll=ScrollMode.AUTO,
            controls=[
                Container(
                    content=Text(
                        self.get_text("select_report_type"),
                        size=18,
                        weight=FontWeight.BOLD,
                    ),
                    padding=Padding.all(20),
                    **self.get_box_style(),
                ),
                Container(height=10),
                report_cards,
            ],
        )

    def show_report_section(self, report_type: str):
        """Show specific report section with filters and preview"""
        self.current_section = report_type

        # Build back button
        back_button = Container(
            content=Row(
                controls=[
                    IconButton(
                        icon=Icons.ARROW_BACK,
                        icon_color=Constants.PRIMARY_COLOR,
                        on_click=lambda e: self.show_home_section(),
                        tooltip=self.get_text("back"),
                    ),
                    Text(
                        self.get_text(f"{report_type}_report"),
                        size=18,
                        weight=FontWeight.BOLD,
                        color=Constants.PRIMARY_COLOR,
                    ),
                ],
                spacing=10,
            ),
            padding=Padding.all(20),
            **self.get_box_style(),
        )

        # Build filter section based on report type
        filter_section = self.build_filter_section(report_type)

        # Build generate button
        generate_button = Container(
            content=Button(
                content=self.get_text("generate_report"),
                icon=Icons.ANALYTICS,
                on_click=lambda e: asyncio.create_task(
                    self.handle_report_generation(report_type)
                ),
                bgcolor=Constants.PRIMARY_COLOR,
                color=Colors.WHITE,
                width=200,
                height=50,
            ),
            padding=Padding.all(20),
            alignment=Alignment.CENTER,
        )

        # Build preview container (initially empty)
        self.preview_container = Container(
            visible=False,
            padding=Padding.all(20),
            **self.get_box_style(),
        )

        self.main_content.content = Column(
            expand=True,
            horizontal_alignment=CrossAxisAlignment.STRETCH,
            scroll=ScrollMode.AUTO,
            controls=[
                back_button,
                Container(height=10),
                filter_section,
                Container(height=10),
                generate_button,
                Container(height=10),
                self.preview_container,
            ],
        )

        try:
            self.main_content.update()
        except Exception:
            pass

    def build_filter_section(self, report_type: str) -> Container:
        """Build filter section based on report type"""
        if report_type == "students":
            filter_form = self.forms.build_students_filter_form()
        elif report_type == "staff_payments":
            filter_form = self.forms.build_staff_payments_filter_form()
        elif report_type == "financial_classroom":
            filter_form = self.forms.build_financial_filter_form("classroom")
        elif report_type == "financial_student":
            filter_form = self.forms.build_financial_filter_form("student")
        elif report_type == "financial_school":
            filter_form = self.forms.build_financial_filter_form("school")
        elif report_type == "cash_register":
            filter_form = self.forms.build_cash_register_filter_form()
        elif report_type == "users":
            # No filters needed for users report
            filter_form = Column(
                controls=[
                    Text(
                        self.get_text("no_filters_needed"),
                        size=14,
                        italic=True,
                    ),
                ],
            )
        else:
            filter_form = Column(controls=[])

        return Container(
            content=filter_form,
            padding=Padding.all(20),
            **self.get_box_style(),
        )

    # ========================================================================
    # REPORT GENERATION
    # ========================================================================

    async def handle_report_generation(self, report_type: str):
        """Handle report generation based on type"""
        if report_type == "students":
            await self.form_handlers.handle_generate_students_report()
        elif report_type == "staff_payments":
            await self.form_handlers.handle_generate_staff_payments_report()
        elif report_type == "financial_classroom":
            await self.form_handlers.handle_generate_financial_classroom_report()
        elif report_type == "financial_student":
            await self.form_handlers.handle_generate_financial_student_report()
        elif report_type == "financial_school":
            await self.form_handlers.handle_generate_school_financial_report()
        elif report_type == "cash_register":
            await self.form_handlers.handle_generate_cash_register_report()
        elif report_type == "users":
            await self.form_handlers.handle_generate_users_report()

    # ========================================================================
    # PERIOD CHANGE HANDLERS
    # ========================================================================

    def on_period_change(self, e):
        """Handle period dropdown change"""
        if hasattr(self.forms, "financial_period_dropdown"):
            is_custom = self.forms.financial_period_dropdown.value == "custom"
            self.forms.financial_start_date.visible = is_custom
            self.forms.financial_end_date.visible = is_custom
            try:
                self.forms.financial_start_date.update()
                self.forms.financial_end_date.update()
            except Exception:
                pass

    def on_staff_payment_period_change(self, e):
        """Handle staff payment period dropdown change"""
        if hasattr(self.forms, "staff_payment_period_dropdown"):
            is_custom = self.forms.staff_payment_period_dropdown.value == "custom"
            self.forms.staff_payment_start_date.visible = is_custom
            self.forms.staff_payment_end_date.visible = is_custom
            try:
                self.forms.staff_payment_start_date.update()
                self.forms.staff_payment_end_date.update()
            except Exception:
                pass

    def on_cash_register_period_change(self, e):
        """Handle cash register period dropdown change"""
        if hasattr(self.forms, "cash_register_period_dropdown"):
            is_custom = self.forms.cash_register_period_dropdown.value == "custom"
            self.forms.cash_register_start_date.visible = is_custom
            self.forms.cash_register_end_date.visible = is_custom
            try:
                self.forms.cash_register_start_date.update()
                self.forms.cash_register_end_date.update()
            except Exception:
                pass

    # ========================================================================
    # STUDENT SEARCH HANDLERS FOR FINANCIAL REPORT
    # ========================================================================

    def handle_financial_student_search_change(self, e):
        """Handle changes in financial student search field"""
        from utils import Utils

        search_text = e.control.value.strip()

        # Hide suggestions if less than 2 characters
        if len(search_text) < 2:
            if hasattr(self.forms, "financial_student_suggestions_container"):
                self.forms.financial_student_suggestions_container.visible = False
                try:
                    self.forms.financial_student_suggestions_container.update()
                except Exception:
                    pass
            return

        # Filter students based on search text
        suggestions = []
        if self.students_list:
            normalized_search = Utils.normalize_text(search_text.lower())

            for student in self.students_list:
                # Get student info
                first_name = student.first_name or ""
                last_name = student.last_name or ""
                surname = getattr(student, "surname", "") or ""
                full_name = f"{first_name} {last_name} {surname}".strip()

                # Normalize for comparison
                normalized_full_name = Utils.normalize_text(full_name.lower())
                normalized_first = Utils.normalize_text(first_name.lower())
                normalized_last = Utils.normalize_text(last_name.lower())
                normalized_surname = Utils.normalize_text(surname.lower())

                # Check if search text matches any part
                if (
                    normalized_search in normalized_full_name
                    or normalized_search in normalized_first
                    or normalized_search in normalized_last
                    or normalized_search in normalized_surname
                ):
                    suggestions.append(student)

        # Display suggestions
        self.display_financial_student_suggestions(suggestions)

    def display_financial_student_suggestions(self, suggestions):
        """Display the list of student suggestions for financial report"""
        if not suggestions:
            if hasattr(self.forms, "financial_student_suggestions_container"):
                self.forms.financial_student_suggestions_container.visible = False
                try:
                    self.forms.financial_student_suggestions_container.update()
                except Exception:
                    pass
            return

        # Create suggestion widgets
        suggestion_widgets = []
        for student in suggestions[:10]:  # Limit to 10 suggestions
            # Get classroom name for this student
            classroom_name = self._get_classroom_name_for_student(student.id_student)

            # Create full name
            surname = getattr(student, "surname", "") or ""
            full_name = f"{student.first_name} {student.last_name} {surname}".strip()

            # Create suggestion tile
            suggestion_tile = ListTile(
                title=Text(full_name, weight=FontWeight.BOLD),
                subtitle=Text(
                    f"Classe: {classroom_name} | Genre: {student.gender}",
                    size=12,
                ),
                leading=Icon(
                    Icons.PERSON,
                    color=(
                        Constants.PRIMARY_COLOR
                        if student.gender == "M"
                        else Colors.PINK
                    ),
                ),
                on_click=lambda e, s=student: self.select_financial_student(s),
                bgcolor=Colors.TRANSPARENT,
                hover_color=Colors.BLUE_50,
            )
            suggestion_widgets.append(suggestion_tile)

        # Update suggestions container
        if hasattr(self.forms, "financial_student_suggestions_container"):
            self.forms.financial_student_suggestions_container.content = ListView(
                controls=suggestion_widgets,
                auto_scroll=False,
                spacing=2,
                expand=True,
            )
            self.forms.financial_student_suggestions_container.visible = True
            try:
                self.forms.financial_student_suggestions_container.update()
            except Exception:
                pass

    def _get_classroom_name_for_student(self, student_id: int) -> str:
        """Get classroom name for a student"""
        try:
            # Find enrollment
            for enrollment in self.enrollments_list:
                if enrollment.student_id == student_id:
                    # Find classroom
                    for classroom in self.classrooms_list:
                        if classroom.id_classroom == enrollment.classroom_id:
                            return classroom.name
        except Exception as e:
            print(f"Error getting classroom name: {e}")
        return "N/A"

    def select_financial_student(self, student):
        """Select a student from suggestions for financial report"""
        self.selected_financial_student_id = student.id_student

        # Build display text for search field
        surname = getattr(student, "surname", "") or ""
        full_name = f"{student.first_name} {student.last_name} {surname}".strip()
        classroom_name = self._get_classroom_name_for_student(student.id_student)

        display_text = f"{full_name}"
        if classroom_name != "N/A":
            display_text += f" - {classroom_name}"

        if hasattr(self.forms, "financial_student_search_field"):
            self.forms.financial_student_search_field.value = display_text

        # Update student info display
        if hasattr(self.forms, "financial_student_info_text"):
            self.forms.financial_student_info_text.value = f"Élève sélectionné: {full_name} | Classe: {classroom_name} | Genre: {student.gender}"

        # Hide suggestions
        if hasattr(self.forms, "financial_student_suggestions_container"):
            self.forms.financial_student_suggestions_container.visible = False

        # Update interface
        try:
            if hasattr(self.forms.financial_student_search_field, "update"):
                self.forms.financial_student_search_field.update()
            if hasattr(self.forms.financial_student_suggestions_container, "update"):
                self.forms.financial_student_suggestions_container.update()
            if hasattr(self.forms.financial_student_info_text, "update"):
                self.forms.financial_student_info_text.update()
        except Exception:
            pass

    def clear_financial_student_search(self, e):
        """Clear financial student search"""
        self.selected_financial_student_id = None

        if hasattr(self.forms, "financial_student_search_field"):
            self.forms.financial_student_search_field.value = ""
        if hasattr(self.forms, "financial_student_info_text"):
            self.forms.financial_student_info_text.value = ""
        if hasattr(self.forms, "financial_student_suggestions_container"):
            self.forms.financial_student_suggestions_container.visible = False

        # Update interface
        try:
            if hasattr(self.forms, "financial_student_search_field") and hasattr(
                self.forms.financial_student_search_field, "update"
            ):
                self.forms.financial_student_search_field.update()
            if hasattr(
                self.forms, "financial_student_suggestions_container"
            ) and hasattr(self.forms.financial_student_suggestions_container, "update"):
                self.forms.financial_student_suggestions_container.update()
            if hasattr(self.forms, "financial_student_info_text") and hasattr(
                self.forms.financial_student_info_text, "update"
            ):
                self.forms.financial_student_info_text.update()
        except Exception:
            pass

    # ========================================================================
    # MAIN UI COMPONENTS
    # ========================================================================

    def build_components(self):
        """Build main UI components"""
        self.loading_indicator = CupertinoActivityIndicator(
            animating=True, color=Constants.PRIMARY_COLOR, radius=50
        )

        self.main_content = Container(
            padding=Padding.symmetric(horizontal=20, vertical=10),
            expand=True,
            content=self.loading_indicator,
            clip_behavior=ClipBehavior.ANTI_ALIAS,
            **self.get_box_style(),
        )

    def build(self) -> Column:
        """Build the main reports screen layout"""
        return Column(
            horizontal_alignment=CrossAxisAlignment.STRETCH,
            controls=[
                Container(
                    content=Row(
                        controls=[
                            Text(
                                value=self.get_text("reports"),
                                size=24,
                                weight=FontWeight.BOLD,
                                color=Constants.PRIMARY_COLOR,
                            ),
                            IconButton(
                                icon=Icons.REFRESH,
                                icon_color=Constants.PRIMARY_COLOR,
                                tooltip=self.get_text("refresh"),
                                on_click=self.refresh_reports_data,
                            ),
                        ],
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                    ),
                    padding=Padding.symmetric(horizontal=20, vertical=10),
                    align=Alignment.CENTER_LEFT,
                    alignment=Alignment.CENTER_LEFT,
                    **self.get_box_style(),
                ),
                self.main_content,
            ],
            expand=True,
        )
