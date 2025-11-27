from flet import *
from core import AppState, Constants
from utils import Utils
import asyncio
from .students_services import StudentsServices
from models import ClassroomModel, StudentModel, EnrollmentModel

from .students_components import StudentsComponents
from .students_forms import StudentsForms
from .students_form_handlers import StudentsFormHandlers
from .students_tables import StudentsTables
from .students_dialogs import StudentsDialogs


class StudentsScreen:
    def __init__(self, app_state: AppState, page: Page):
        self.app_state = app_state
        self.translations = app_state.translations
        self.services = StudentsServices(app_state)
        self.page = page

        # Pagination and search state
        self.students_data = []
        self.classrooms_data = []
        self.enrollments_data = []
        self.filtered_students = []
        self.current_page = 1
        self.items_per_page = 10
        self.search_query = ""
        self.selected_classroom_filter = "all"
        self.selected_gender_filter = "all"

        # Initialize modules
        self.forms = StudentsForms(self)
        self.form_handlers = StudentsFormHandlers(self)
        self.tables = StudentsTables(self)
        self.dialogs = StudentsDialogs(self)

        self.build_components()
        self.forms.build_add_form_components()
        self.tables.build_table_components()
        self.dialogs.build_edit_dialog()
        self.dialogs.build_delete_dialog()
        self.dialogs.build_import_dialog()

    async def on_mount(self):
        self.translations = self.app_state.translations
        await self.load_data()

    def refresh_students_data(self, e):
        self.main_content.content = self.loading_indicator
        self.main_content.update()
        asyncio.create_task(self.load_data())

    def get_text(self, key: str) -> str:
        return self.app_state.translations.get(key, key)

    def propagate_classrooms(self, classrooms: list[ClassroomModel]):
        options = [
            DropdownOption(key=str(c.id_classroom), text=c.name) for c in classrooms
        ]
        self.classroom_form.options = options

    async def load_data(self):
        students_status, students_data = await self.services.load_students_data()
        classrooms_status, classrooms_data = await self.services.load_classrooms_data()
        enrollments_status, enrollments_data = (
            await self.services.load_enrollments_data()
        )

        # Store data
        self.students_data = students_data if students_status else []
        self.classrooms_data = classrooms_data if classrooms_status else []
        self.enrollments_data = enrollments_data if enrollments_status else []

        # Reset pagination and filters
        self.current_page = 1
        self.search_query = ""
        self.search_field.value = ""
        self.selected_classroom_filter = "all"
        self.selected_gender_filter = "all"

        # Update filter dropdowns
        self.tables.update_classroom_filter_options()
        if hasattr(self, "classroom_filter_dropdown"):
            self.classroom_filter_dropdown.value = "all"
        if hasattr(self, "gender_filter_dropdown"):
            self.gender_filter_dropdown.value = "all"

        # Filter students
        self.tables.apply_filters()

        self.main_content.content = Column(
            expand=True,
            horizontal_alignment=CrossAxisAlignment.STRETCH,
            scroll=ScrollMode.AUTO,
            controls=[
                Row(
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    spacing=20,
                    controls=[
                        StudentsComponents.create_stat_card(
                            title=self.get_text("total_students"),
                            value=str(len(students_data)) if students_status else "N/A",
                            icon=Icons.SCHOOL,
                            color=Constants.PRIMARY_COLOR,
                        ),
                        StudentsComponents.create_stat_card(
                            title=self.get_text("total_classrooms"),
                            value=(
                                str(len(classrooms_data))
                                if classrooms_status
                                else "N/A"
                            ),
                            icon=Icons.CLASS_,
                            color=Constants.SECONDARY_COLOR,
                        ),
                        StudentsComponents.create_stat_card(
                            title=self.get_text("average_students_per_classroom"),
                            value=(
                                str(round(len(students_data) / len(classrooms_data), 2))
                                if students_status
                                and classrooms_status
                                and len(classrooms_data) > 0
                                else "N/A"
                            ),
                            icon=Icons.GROUP,
                            color=Colors.ORANGE,
                        ),
                    ],
                ),
                self.container_form,
                Container(
                    content=Text(
                        self.get_text("students_list"),
                        size=18,
                        weight=FontWeight.BOLD,
                        color=Constants.PRIMARY_COLOR,
                    ),
                    margin=Margin(top=20, bottom=10),
                ),
                self.search_and_pagination_container,
                self.students_table_container,
            ],
        )
        if classrooms_status:
            self.propagate_classrooms(classrooms_data)

        self.tables.update_table()

        try:
            self.main_content.update()
        except Exception as e:
            # print("Error updating main content:", e)
            pass

    def show_error_snackbar(self, message: str):
        """Show error snackbar"""
        try:
            self.page.show_snack_bar(
                SnackBar(
                    content=Text(message),
                    bgcolor=Colors.RED,
                )
            )
        except:
            print(f"Error: {message}")

    def show_success_snackbar(self, message: str):
        """Show success snackbar"""
        try:
            self.page.show_snack_bar(
                SnackBar(
                    content=Text(message),
                    bgcolor=Colors.GREEN,
                )
            )
        except:
            print(f"Success: {message}")

    def build_components(self):
        self.loading_indicator = CupertinoActivityIndicator(
            animating=True, color=Constants.PRIMARY_COLOR, radius=50
        )

        self.add_button = Button(
            icon=Icons.ADD,
            tooltip=self.get_text("add_student"),
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                bgcolor=Constants.PRIMARY_COLOR,
                padding=Padding(10, 20, 10, 20),
                color="white",
            ),
            on_click=self.form_handlers.open_add_form,
            content=self.get_text("add_student"),
        )

        self.load_file_button = Button(
            icon=Icons.ADD,
            tooltip=self.get_text("load_from_file"),
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                bgcolor=Colors.ORANGE,
                padding=Padding(10, 20, 10, 20),
                color="white",
            ),
            on_click=self.dialogs.open_import_dialog,
            content=self.get_text("load_from_file"),
        )

        self.main_content = Container(
            padding=Padding.symmetric(horizontal=20, vertical=10),
            expand=True,
            content=self.loading_indicator,
            clip_behavior=ClipBehavior.ANTI_ALIAS,
            **StudentsComponents.get_box_style(),
        )

    def build(self) -> Control:
        return Column(
            horizontal_alignment=CrossAxisAlignment.STRETCH,
            controls=[
                Container(
                    content=Row(
                        controls=[
                            Text(
                                value=self.get_text("students_management"),
                                size=24,
                                weight=FontWeight.BOLD,
                                color=Constants.PRIMARY_COLOR,
                            ),
                            Row(
                                controls=[
                                    self.add_button,
                                    self.load_file_button,
                                    IconButton(
                                        icon=Icons.REFRESH,
                                        icon_color=Constants.PRIMARY_COLOR,
                                        tooltip=self.get_text("refresh"),
                                        on_click=self.refresh_students_data,
                                    ),
                                ],
                                spacing=10,
                                alignment=MainAxisAlignment.END,
                                vertical_alignment=CrossAxisAlignment.CENTER,
                            ),
                        ],
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                    ),
                    padding=Padding.symmetric(horizontal=20, vertical=10),
                    align=Alignment.CENTER_LEFT,
                    alignment=Alignment.CENTER_LEFT,
                    **StudentsComponents.get_box_style(),
                ),
                self.main_content,
            ],
            expand=True,
        )
