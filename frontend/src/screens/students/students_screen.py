from flet import *  # type: ignore
from core import AppState, Constants
from utils import Utils
import asyncio
from .students_services import StudentsServices
from models import ClassroomModel, StudentModel, EnrollmentModel


class StudentsScreen:
    def __init__(self, app_state: AppState, page: Page):
        self.app_state = app_state
        self.translations = app_state.translations
        self.services = StudentsServices(app_state)
        self.page = page

        # Pagination and search state
        self.students_data = []
        self.classrooms_data = []
        self.filtered_students = []
        self.current_page = 1
        self.items_per_page = 10
        self.search_query = ""
        self.selected_classroom_filter = "all"
        self.selected_gender_filter = "all"

        self.build_components()
        self._build_add_form_components()
        self._build_table_components()
        self._build_edit_dialog()

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
        self._update_classroom_filter_options()
        if hasattr(self, "classroom_filter_dropdown"):
            self.classroom_filter_dropdown.value = "all"
        if hasattr(self, "gender_filter_dropdown"):
            self.gender_filter_dropdown.value = "all"

        # Filter students
        self._apply_filters()

        self.main_content.content = Column(
            expand=True,
            horizontal_alignment=CrossAxisAlignment.STRETCH,
            scroll=ScrollMode.AUTO,
            controls=[
                Row(
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    spacing=20,
                    controls=[
                        self.create_stat_card(
                            title=self.get_text("total_students"),
                            value=str(len(students_data)) if students_status else "N/A",
                            icon=Icons.SCHOOL,
                            color=Constants.PRIMARY_COLOR,
                        ),
                        self.create_stat_card(
                            title=self.get_text("total_classrooms"),
                            value=(
                                str(len(classrooms_data))
                                if classrooms_status
                                else "N/A"
                            ),
                            icon=Icons.CLASS_,
                            color=Constants.SECONDARY_COLOR,
                        ),
                        self.create_stat_card(
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

        self._update_table()

        try:
            self.main_content.update()
        except Exception as e:
            # print("Error updating main content:", e)
            pass

    @staticmethod
    def get_box_style() -> dict:
        return {
            "border_radius": BorderRadius.all(10),
            "shadow": BoxShadow(color="black12", blur_radius=5, offset=Offset(0, 2)),
            "bgcolor": "#f8faff",
        }

    def _build_add_form_components(self):
        self.full_name_field_form = TextField(
            label=self.get_text("full_name"),
            hint_text=self.get_text("enter_full_name"),
            autofocus=True,
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=2,
            helper=self.get_text("full_name_helper"),
        )

        self.birth_date_field_form = TextField(
            label=self.get_text("birth_date"),
            hint_text=self.get_text("enter_birth_date"),
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            keyboard_type=KeyboardType.DATETIME,
            value="01-01-2000",
            expand=1,
            helper=self.get_text("date_format_dd_mm_yyyy"),
        )

        self.classroom_form = Dropdown(
            label=self.get_text("classroom"),
            border_radius=BorderRadius.all(5),
            options=[],
            expand=1,
            helper_text=self.get_text("select_classroom"),
            width=float("inf"),
            menu_width=200,
        )

        self.gender_form = Dropdown(
            label=self.get_text("gender"),
            border_radius=BorderRadius.all(5),
            options=[
                DropdownOption(key="male", text=self.get_text("male")),
                DropdownOption(key="female", text=self.get_text("female")),
            ],
            expand=1,
            helper_text=self.get_text("select_gender"),
            width=float("inf"),
            menu_width=150,
        )

        self.address_field_form = TextField(
            label=self.get_text("address"),
            hint_text=self.get_text("enter_address"),
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=2,
            helper=self.get_text("address_helper"),
            multiline=True,
        )

        self.parent_contact_field_form = TextField(
            label=self.get_text("parent_contact"),
            hint_text=self.get_text("enter_parent_contact"),
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=2,
            helper=self.get_text("parent_contact_helper"),
            multiline=True,
        )

        self.button_submit_form = Button(
            content=self.get_text("submit"),
            icon=Icons.SAVE,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                bgcolor=Constants.PRIMARY_COLOR,
                padding=Padding(10, 20, 10, 20),
                color="white",
            ),
        )

        self.button_cancel_form = Button(
            content=self.get_text("cancel"),
            icon=Icons.CANCEL,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                bgcolor=Constants.CANCEL_COLOR,
                padding=Padding(10, 20, 10, 20),
                color="white",
            ),
            on_click=self._close_add_form,
        )

        self.container_form = Container(
            content=Column(
                horizontal_alignment=CrossAxisAlignment.STRETCH,
                controls=[
                    Text(
                        value=self.get_text("add_student"),
                        style=TextStyle(
                            size=18,
                            weight=FontWeight.BOLD,
                            color=Constants.PRIMARY_COLOR,
                        ),
                    ),
                    Row(
                        controls=[
                            self.full_name_field_form,
                            self.birth_date_field_form,
                            self.classroom_form,
                        ],
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                    ),
                    Row(
                        controls=[
                            self.gender_form,
                            self.address_field_form,
                            self.parent_contact_field_form,
                        ],
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                    ),
                    Row(
                        controls=[
                            self.button_submit_form,
                            self.button_cancel_form,
                        ],
                        alignment=MainAxisAlignment.END,
                    ),
                ],
            ),
            visible=False,
            padding=Padding.all(15),
            margin=Margin(top=20),
            **self.get_box_style(),
        )

    def _clear_form(self):
        self.full_name_field_form.value = ""
        self.birth_date_field_form.value = "01-01-2000"
        if self.classroom_form.options:
            self.classroom_form.value = self.classroom_form.options[0].key
        self.gender_form.value = None
        self.address_field_form.value = ""
        self.parent_contact_field_form.value = ""
        self.full_name_field_form.update()
        self.birth_date_field_form.update()
        self.classroom_form.update()
        self.gender_form.update()
        self.address_field_form.update()
        self.parent_contact_field_form.update()

    def _open_add_form(self, e):
        self.container_form.visible = True
        self.add_button.icon = Icons.CLOSE
        self.add_button.tooltip = self.get_text("close_form")
        self.add_button.content = self.get_text("close_form")
        self.add_button.style.bgcolor = Constants.CANCEL_COLOR
        self.add_button.on_click = self._close_add_form
        self.add_button.update()
        self.container_form.update()

    def _close_add_form(self, e):
        self.container_form.visible = False
        self.add_button.icon = Icons.ADD
        self.add_button.style.bgcolor = Constants.PRIMARY_COLOR
        self.add_button.tooltip = self.get_text("add_student")
        self.add_button.content = self.get_text("add_student")
        self.add_button.on_click = self._open_add_form
        self._clear_form()
        self.add_button.update()
        self.container_form.update()

    def _build_table_components(self):
        """Build the students table and pagination components"""
        self.search_field = TextField(
            hint_text=self.get_text("search_by_name"),
            prefix_icon=Icons.SEARCH,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            on_change=self._on_search_change,
            expand=True,
        )

        self.classroom_filter_dropdown = Dropdown(
            label=self.get_text("filter_by_classroom"),
            value="all",
            options=[
                DropdownOption(key="all", text=self.get_text("all_classrooms")),
            ],
            width=200,
            on_change=self._on_classroom_filter_change,
        )

        self.gender_filter_dropdown = Dropdown(
            label=self.get_text("filter_by_gender"),
            value="all",
            options=[
                DropdownOption(key="all", text=self.get_text("all_genders")),
                DropdownOption(key="male", text=self.get_text("male")),
                DropdownOption(key="female", text=self.get_text("female")),
            ],
            width=150,
            on_change=self._on_gender_filter_change,
        )

        self.items_per_page_dropdown = Dropdown(
            label=self.get_text("items_per_page"),
            value="10",
            options=[
                DropdownOption(key="5", text="5"),
                DropdownOption(key="10", text="10"),
                DropdownOption(key="20", text="20"),
                DropdownOption(key="50", text="50"),
            ],
            width=150,
            on_change=self._on_items_per_page_change,
        )

        self.page_info_text = Text(
            value="",
            size=14,
            color=Constants.PRIMARY_COLOR,
        )

        self.prev_page_button = IconButton(
            icon=Icons.ARROW_BACK,
            icon_color=Constants.PRIMARY_COLOR,
            tooltip=self.get_text("previous"),
            on_click=self._go_to_prev_page,
            disabled=True,
        )

        self.next_page_button = IconButton(
            icon=Icons.ARROW_FORWARD,
            icon_color=Constants.PRIMARY_COLOR,
            tooltip=self.get_text("next"),
            on_click=self._go_to_next_page,
            disabled=True,
        )

        self.search_and_pagination_container = Container(
            content=Column(
                controls=[
                    Row(
                        controls=[
                            self.search_field,
                            self.classroom_filter_dropdown,
                            self.gender_filter_dropdown,
                        ],
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    Row(
                        controls=[
                            self.items_per_page_dropdown,
                            Row(
                                controls=[
                                    self.prev_page_button,
                                    self.page_info_text,
                                    self.next_page_button,
                                ],
                                alignment=MainAxisAlignment.END,
                            ),
                        ],
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                    ),
                ],
                spacing=10,
            ),
            padding=Padding.all(10),
            **self.get_box_style(),
        )

        self.students_table_container = Container(
            content=Column(
                controls=[],
                scroll=ScrollMode.AUTO,
            ),
            padding=Padding.all(10),
            **self.get_box_style(),
        )

    def _build_edit_dialog(self):
        """Build the edit student dialog"""
        # Create form fields for edit dialog
        self.edit_first_name_field = TextField(
            label=self.get_text("first_name"),
            hint_text=self.get_text("enter_first_name"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
        )

        self.edit_last_name_field = TextField(
            label=self.get_text("last_name"),
            hint_text=self.get_text("enter_last_name"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
        )

        self.edit_surname_field = TextField(
            label=self.get_text("surname"),
            hint_text=self.get_text("enter_surname"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
        )

        self.edit_birth_date_field = TextField(
            label=self.get_text("birth_date"),
            hint_text=self.get_text("enter_birth_date"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            keyboard_type=KeyboardType.DATETIME,
            expand=1,
        )

        self.edit_gender_dropdown = Dropdown(
            label=self.get_text("gender"),
            border_radius=BorderRadius.all(5),
            options=[
                DropdownOption(key="male", text=self.get_text("male")),
                DropdownOption(key="female", text=self.get_text("female")),
            ],
            expand=1,
            width=float("inf"),
            menu_width=150,
        )

        self.edit_classroom_dropdown = Dropdown(
            label=self.get_text("classroom"),
            border_radius=BorderRadius.all(5),
            options=[],
            expand=1,
            width=float("inf"),
            menu_width=250,
        )

        self.edit_address_field = TextField(
            label=self.get_text("address"),
            hint_text=self.get_text("enter_address"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            multiline=True,
            min_lines=2,
            max_lines=3,
            expand=1,
        )

        self.edit_parent_contact_field = TextField(
            label=self.get_text("parent_contact"),
            hint_text=self.get_text("enter_parent_contact"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            multiline=True,
            min_lines=2,
            max_lines=3,
            expand=1,
        )

        # Create the dialog
        self.edit_dialog = AlertDialog(
            modal=True,
            scrollable=True,
            bgcolor="#f8faff",
            title=Container(
                content=Text(
                    self.get_text("edit_student"),
                    weight=FontWeight.BOLD,
                    color="white",
                ),
                padding=Padding.symmetric(horizontal=20, vertical=10),
                align=Alignment.CENTER_LEFT,
                alignment=Alignment.CENTER_LEFT,
                border_radius=BorderRadius.all(10),
                bgcolor=Constants.PRIMARY_COLOR,
            ),
            content=Container(
                content=Column(
                    controls=[
                        Row(
                            controls=[
                                self.edit_first_name_field,
                                self.edit_last_name_field,
                            ],
                            spacing=10,
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        Row(
                            controls=[
                                self.edit_surname_field,
                                self.edit_birth_date_field,
                            ],
                            spacing=10,
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        Row(
                            controls=[
                                self.edit_gender_dropdown,
                                self.edit_classroom_dropdown,
                            ],
                            spacing=10,
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        Row(
                            controls=[
                                self.edit_address_field,
                                self.edit_parent_contact_field,
                            ],
                            spacing=10,
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                        ),
                    ],
                    spacing=15,
                    tight=True,
                ),
                width=600,
                padding=Padding.all(20),
                align=Alignment.CENTER_LEFT,
                alignment=Alignment.CENTER_LEFT,
                clip_behavior=ClipBehavior.HARD_EDGE,
                **self.get_box_style(),
            ),
            actions=[
                Button(
                    content=Text(self.get_text("cancel")),
                    on_click=self._close_edit_dialog,
                    style=ButtonStyle(
                        shape=RoundedRectangleBorder(radius=5),
                        bgcolor=Constants.CANCEL_COLOR,
                        padding=Padding(10, 20, 10, 20),
                        color="white",
                    ),
                ),
                Button(
                    content=Text(self.get_text("update")),
                    on_click=self._save_student_changes,
                    style=ButtonStyle(
                        shape=RoundedRectangleBorder(radius=5),
                        bgcolor=Constants.PRIMARY_COLOR,
                        padding=Padding(10, 20, 10, 20),
                        color="white",
                    ),
                ),
            ],
            actions_alignment=MainAxisAlignment.END,
        )

    def _apply_filters(self):
        """Apply search and filters to students data"""
        if not self.students_data:
            self.filtered_students = []
            return

        query = self.search_query.lower().strip()

        # Start with all students
        filtered = self.students_data.copy()

        # Apply text search filter
        if query:
            filtered = [
                student
                for student in filtered
                if (
                    query in student.first_name.lower()
                    or query in student.last_name.lower()
                    or query in student.surname.lower()
                )
            ]

        # Apply classroom filter
        if self.selected_classroom_filter != "all":
            classroom_id = int(self.selected_classroom_filter)
            # Get students enrolled in the selected classroom
            enrolled_student_ids = [
                enrollment.student_id
                for enrollment in self.enrollments_data
                if enrollment.classroom_id == classroom_id
            ]
            filtered = [
                student
                for student in filtered
                if student.id_student in enrolled_student_ids
            ]

        # Apply gender filter
        if self.selected_gender_filter != "all":
            filtered = [
                student
                for student in filtered
                if student.gender.lower() == self.selected_gender_filter.lower()
            ]

        self.filtered_students = filtered

    def _update_classroom_filter_options(self):
        """Update classroom filter dropdown options"""
        if not hasattr(self, "classroom_filter_dropdown"):
            return

        options = [
            DropdownOption(key="all", text=self.get_text("all_classrooms")),
        ]

        for classroom in self.classrooms_data:
            options.append(
                DropdownOption(key=str(classroom.id_classroom), text=classroom.name)
            )

        self.classroom_filter_dropdown.options = options

    def _on_search_change(self, e):
        """Handle search field change"""
        self.search_query = e.control.value
        self.current_page = 1
        self._apply_filters()
        self._update_table()

    def _on_classroom_filter_change(self, e):
        """Handle classroom filter change"""
        self.selected_classroom_filter = e.control.value
        self.current_page = 1
        self._apply_filters()
        self._update_table()

    def _on_gender_filter_change(self, e):
        """Handle gender filter change"""
        self.selected_gender_filter = e.control.value
        self.current_page = 1
        self._apply_filters()
        self._update_table()

    def _on_items_per_page_change(self, e):
        """Handle items per page dropdown change"""
        self.items_per_page = int(e.control.value)
        self.current_page = 1
        self._update_table()

    def _go_to_prev_page(self, e):
        """Go to previous page"""
        if self.current_page > 1:
            self.current_page -= 1
            self._update_table()

    def _go_to_next_page(self, e):
        """Go to next page"""
        total_pages = self._get_total_pages()
        if self.current_page < total_pages:
            self.current_page += 1
            self._update_table()

    def _get_total_pages(self):
        """Calculate total number of pages"""
        if not self.filtered_students:
            return 1
        return max(
            1,
            (len(self.filtered_students) + self.items_per_page - 1)
            // self.items_per_page,
        )

    def _get_paginated_students(self):
        """Get students for current page"""
        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = start_idx + self.items_per_page
        return self.filtered_students[start_idx:end_idx]

    def _get_classroom_name(self, student_id) -> str:
        """Get classroom name for a student"""
        for enrollment in self.enrollments_data:
            if enrollment.student_id == student_id:
                for classroom in self.classrooms_data:
                    if classroom.id_classroom == enrollment.classroom_id:
                        return classroom.name
        return "N/A"

    def _get_birth_year(self, date_of_birth: str) -> str:
        """Extract birth year from date string"""
        try:
            # Assuming date format is YY-MM-DD
            parts = date_of_birth.replace("/", "-").split("-")
            if len(parts) == 3:
                return parts[0]  # Year is the first part
        except:
            pass
        return "N/A"

    def _on_edit_student(self, student_id):
        """Handle edit student button click"""

        def handler(e):
            self._open_edit_dialog(student_id)

        return handler

    def _on_delete_student(self, student_id):
        """Handle delete student button click"""

        def handler(e):
            # TODO: Implement delete functionality
            print(f"Delete student {student_id}")
            # self.page.show_snack_bar(
            #     SnackBar(
            #         content=Text(f"Suppression de l'élève {student_id} (à implémenter)")
            #     )
            # )

        return handler

    def _open_edit_dialog(self, student_id: int):
        """Open edit dialog and populate with student data"""
        # Find the student
        student = None
        for s in self.students_data:
            if s.id_student == student_id:
                student = s
                break

        if not student:
            return

        # Store the current student being edited
        self.current_editing_student_id = student_id

        # Populate form fields
        self.edit_first_name_field.value = student.first_name
        self.edit_last_name_field.value = student.last_name
        self.edit_surname_field.value = student.surname
        self.edit_birth_date_field.value = student.date_of_birth
        self.edit_gender_dropdown.value = student.gender.lower()
        self.edit_address_field.value = student.address
        self.edit_parent_contact_field.value = student.parent_contact

        # Populate classroom dropdown
        classroom_options = [
            DropdownOption(key=str(c.id_classroom), text=c.name)
            for c in self.classrooms_data
        ]
        self.edit_classroom_dropdown.options = classroom_options

        # Find and set the current classroom
        current_classroom_id = None
        for enrollment in self.enrollments_data:
            if enrollment.student_id == student_id:
                current_classroom_id = enrollment.classroom_id
                break

        if current_classroom_id:
            self.edit_classroom_dropdown.value = str(current_classroom_id)

        # Open the dialog
        self.page.show_dialog(self.edit_dialog)
        self.page.update()

    def _close_edit_dialog(self, e=None):
        """Close the edit dialog"""
        self.edit_dialog.open = False
        self.page.update()

    async def _save_student_changes(self, e):
        """Save changes to the student"""
        try:
            # Get updated values
            updated_student = StudentModel(
                id_student=self.current_editing_student_id,
                first_name=self.edit_first_name_field.value.strip(),
                last_name=self.edit_last_name_field.value.strip(),
                surname=self.edit_surname_field.value.strip(),
                gender=self.edit_gender_dropdown.value,
                date_of_birth=self.edit_birth_date_field.value.strip(),
                address=self.edit_address_field.value.strip(),
                parent_contact=self.edit_parent_contact_field.value.strip(),
            )

            # TODO: Call API to update student
            # success = await self.services.update_student(updated_student)

            # For now, update locally
            for i, student in enumerate(self.students_data):
                if student.id_student == self.current_editing_student_id:
                    self.students_data[i] = updated_student
                    break

            # Update enrollment if classroom changed
            selected_classroom_id = int(self.edit_classroom_dropdown.value)
            for enrollment in self.enrollments_data:
                if enrollment.student_id == self.current_editing_student_id:
                    enrollment.classroom_id = selected_classroom_id
                    break

            # Close dialog
            self._close_edit_dialog()

            # Refresh the table
            self._apply_filters()
            self._update_table()

            # Show success message
            self.page.show_snack_bar(
                SnackBar(
                    content=Text(self.get_text("student_updated")),
                    bgcolor=Colors.GREEN,
                )
            )

        except Exception as ex:
            print(f"Error updating student: {ex}")
            self.page.show_snack_bar(
                SnackBar(
                    content=Text(self.get_text("error_updating_student")),
                    bgcolor=Colors.RED,
                )
            )

    def _create_table_header(self):
        """Create table header row"""
        return Container(
            content=Row(
                controls=[
                    Container(
                        content=Text(
                            self.get_text("full_name"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=3,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.get_text("gender"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=1,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.get_text("classroom"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.get_text("year_of_birth"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=1,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.get_text("actions"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                ],
            ),
            bgcolor=Constants.PRIMARY_COLOR,
            border_radius=BorderRadius.only(top_left=10, top_right=10),
        )

    def _create_table_row(self, student: StudentModel, index):
        """Create a table row for a student"""
        full_name = f"{student.last_name} {student.surname} {student.first_name}"
        gender_text = (
            self.get_text("male")
            if student.gender.lower() == "male"
            else self.get_text("female")
        )
        classroom_name = self._get_classroom_name(student.id_student)
        birth_year = self._get_birth_year(student.date_of_birth)

        row_color = "#f8faff" if index % 2 == 0 else "#ffffff"

        return Container(
            content=Row(
                controls=[
                    Container(
                        content=Text(full_name, size=14),
                        expand=3,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(gender_text, size=14),
                        expand=1,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(classroom_name, size=14),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(birth_year, size=14),
                        expand=1,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Row(
                            controls=[
                                IconButton(
                                    icon=Icons.EDIT,
                                    icon_color=Constants.PRIMARY_COLOR,
                                    tooltip=self.get_text("edit"),
                                    on_click=self._on_edit_student(student.id_student),
                                ),
                                IconButton(
                                    icon=Icons.DELETE,
                                    icon_color=Constants.CANCEL_COLOR,
                                    tooltip=self.get_text("delete"),
                                    on_click=self._on_delete_student(
                                        student.id_student
                                    ),
                                ),
                            ],
                            spacing=5,
                        ),
                        expand=2,
                        padding=Padding.all(5),
                    ),
                ],
            ),
            bgcolor=row_color,
        )

    def _update_table(self):
        """Update the students table with current data"""
        total_pages = self._get_total_pages()
        paginated_students = self._get_paginated_students()

        # Update pagination info
        start_item = (self.current_page - 1) * self.items_per_page + 1
        end_item = min(
            self.current_page * self.items_per_page, len(self.filtered_students)
        )
        self.page_info_text.value = f"{self.get_text('page')} {self.current_page} {self.get_text('of')} {total_pages} ({start_item}-{end_item} / {len(self.filtered_students)})"

        # Update pagination buttons
        self.prev_page_button.disabled = self.current_page <= 1
        self.next_page_button.disabled = self.current_page >= total_pages

        # Build table content
        table_controls = [self._create_table_header()]

        if not paginated_students:
            # No students found message
            table_controls.append(
                Container(
                    content=Column(
                        controls=[
                            Icon(Icons.SEARCH_OFF, size=60, color=Colors.GREY_400),
                            Text(
                                self.get_text("no_students_found"),
                                size=18,
                                weight=FontWeight.BOLD,
                                color=Colors.GREY_600,
                            ),
                            Text(
                                self.get_text("no_students_message"),
                                size=14,
                                color=Colors.GREY_500,
                            ),
                        ],
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    padding=Padding.all(40),
                    alignment=Alignment(0, 0),
                )
            )
        else:
            # Add student rows
            for index, student in enumerate(paginated_students):
                table_controls.append(self._create_table_row(student, index))

        self.students_table_container.content = Column(
            controls=table_controls,
            scroll=ScrollMode.AUTO,
            spacing=0,
        )

        try:
            self.search_and_pagination_container.update()
            self.students_table_container.update()
        except Exception as e:
            # print("Error updating table:", e)
            pass

    def create_stat_card(
        self, title: str, value: str, icon: str, color: str, subtitle: str = None
    ) -> Control:
        """Créer une carte de statistique améliorée"""
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
            # width=250,
            height=100,
            **self.get_box_style(),
        )

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
            on_click=self._open_add_form,
            content=self.get_text("add_student"),
        )

        self.main_content = Container(
            padding=Padding.symmetric(horizontal=20, vertical=10),
            expand=True,
            content=self.loading_indicator,
            clip_behavior=ClipBehavior.ANTI_ALIAS,
            **self.get_box_style(),
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
                    **self.get_box_style(),
                ),
                self.main_content,
            ],
            expand=True,
        )
