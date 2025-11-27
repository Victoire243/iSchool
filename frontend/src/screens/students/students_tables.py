from flet import *
from core import Constants
from models import StudentModel
from .students_components import StudentsComponents


class StudentsTables:
    def __init__(self, students_screen):
        self.screen = students_screen

    def build_table_components(self):
        """Build the students table and pagination components"""
        self.screen.search_field = TextField(
            hint_text=self.screen.get_text("search_by_name"),
            prefix_icon=Icons.SEARCH,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            on_change=self.on_search_change,
            expand=True,
        )

        self.screen.classroom_filter_dropdown = Dropdown(
            label=self.screen.get_text("filter_by_classroom"),
            value="all",
            options=[
                DropdownOption(key="all", text=self.screen.get_text("all_classrooms")),
            ],
            width=200,
            on_change=self.on_classroom_filter_change,
        )

        self.screen.gender_filter_dropdown = Dropdown(
            label=self.screen.get_text("filter_by_gender"),
            value="all",
            options=[
                DropdownOption(key="all", text=self.screen.get_text("all_genders")),
                DropdownOption(key="male", text=self.screen.get_text("male")),
                DropdownOption(key="female", text=self.screen.get_text("female")),
            ],
            width=150,
            on_change=self.on_gender_filter_change,
        )

        self.screen.items_per_page_dropdown = Dropdown(
            label=self.screen.get_text("items_per_page"),
            value="10",
            options=[
                DropdownOption(key="5", text="5"),
                DropdownOption(key="10", text="10"),
                DropdownOption(key="20", text="20"),
                DropdownOption(key="50", text="50"),
            ],
            width=150,
            on_change=self.on_items_per_page_change,
        )

        self.screen.page_info_text = Text(
            value="",
            size=14,
            color=Constants.PRIMARY_COLOR,
        )

        self.screen.prev_page_button = IconButton(
            icon=Icons.ARROW_BACK,
            icon_color=Constants.PRIMARY_COLOR,
            tooltip=self.screen.get_text("previous"),
            on_click=self.go_to_prev_page,
            disabled=True,
        )

        self.screen.next_page_button = IconButton(
            icon=Icons.ARROW_FORWARD,
            icon_color=Constants.PRIMARY_COLOR,
            tooltip=self.screen.get_text("next"),
            on_click=self.go_to_next_page,
            disabled=True,
        )

        self.screen.search_and_pagination_container = Container(
            content=Column(
                controls=[
                    Row(
                        controls=[
                            self.screen.search_field,
                            self.screen.classroom_filter_dropdown,
                            self.screen.gender_filter_dropdown,
                        ],
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    Row(
                        controls=[
                            self.screen.items_per_page_dropdown,
                            Row(
                                controls=[
                                    self.screen.prev_page_button,
                                    self.screen.page_info_text,
                                    self.screen.next_page_button,
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
            **StudentsComponents.get_box_style(),
        )

        self.screen.students_table_container = Container(
            content=Column(
                controls=[],
                scroll=ScrollMode.AUTO,
            ),
            padding=Padding.all(10),
            **StudentsComponents.get_box_style(),
        )

    def create_table_header(self):
        """Create table header row"""
        return Container(
            content=Row(
                controls=[
                    Container(
                        content=Text(
                            self.screen.get_text("full_name"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=3,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.screen.get_text("gender"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=1,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.screen.get_text("classroom"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.screen.get_text("year_of_birth"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=1,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.screen.get_text("actions"),
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

    def create_table_row(self, student: StudentModel, index):
        """Create a table row for a student"""
        full_name = f"{student.last_name} {student.surname} {student.first_name}"
        gender_text = (
            self.screen.get_text("male")
            if student.gender.lower().startswith("m")
            else self.screen.get_text("female")
        )
        classroom_name = self.get_classroom_name(student.id_student)
        birth_year = self.get_birth_year(student.date_of_birth)

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
                                    tooltip=self.screen.get_text("edit"),
                                    on_click=lambda e, s=student: self.screen.dialogs.open_edit_dialog(
                                        s
                                    ),
                                ),
                                IconButton(
                                    icon=Icons.DELETE,
                                    icon_color=Constants.CANCEL_COLOR,
                                    tooltip=self.screen.get_text("delete"),
                                    on_click=lambda e, s=student: self.screen.dialogs.open_delete_dialog(
                                        s
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
            on_click=lambda e, s=student: self.screen.dialogs.show_student_details_dialog(
                s
            ),
            ink=True,
        )

    def update_table(self):
        """Update the students table with current data"""
        total_pages = self.get_total_pages()
        paginated_students = self.get_paginated_students()

        # Update pagination info
        start_item = (self.screen.current_page - 1) * self.screen.items_per_page + 1
        end_item = min(
            self.screen.current_page * self.screen.items_per_page,
            len(self.screen.filtered_students),
        )
        self.screen.page_info_text.value = f"{self.screen.get_text('page')} {self.screen.current_page} {self.screen.get_text('of')} {total_pages} ({start_item}-{end_item} / {len(self.screen.filtered_students)})"

        # Update pagination buttons
        self.screen.prev_page_button.disabled = self.screen.current_page <= 1
        self.screen.next_page_button.disabled = self.screen.current_page >= total_pages

        # Build table content
        table_controls = [self.create_table_header()]

        if not paginated_students:
            # No students found message
            table_controls.append(
                Container(
                    content=Column(
                        controls=[
                            Icon(Icons.SEARCH_OFF, size=60, color=Colors.GREY_400),
                            Text(
                                self.screen.get_text("no_students_found"),
                                size=18,
                                weight=FontWeight.BOLD,
                                color=Colors.GREY_600,
                            ),
                            Text(
                                self.screen.get_text("no_students_message"),
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
                table_controls.append(self.create_table_row(student, index))

        self.screen.students_table_container.content = Column(
            controls=table_controls,
            scroll=ScrollMode.AUTO,
            spacing=0,
        )

        try:
            self.screen.search_and_pagination_container.update()
            self.screen.students_table_container.update()
        except Exception as e:
            # print("Error updating table:", e)
            pass

    def on_search_change(self, e):
        """Handle search field change"""
        self.screen.search_query = e.control.value
        self.screen.current_page = 1
        self.apply_filters()
        self.update_table()

    def on_classroom_filter_change(self, e):
        """Handle classroom filter change"""
        self.screen.selected_classroom_filter = e.control.value
        self.screen.current_page = 1
        self.apply_filters()
        self.update_table()

    def on_gender_filter_change(self, e):
        """Handle gender filter change"""
        self.screen.selected_gender_filter = e.control.value
        self.screen.current_page = 1
        self.apply_filters()
        self.update_table()

    def on_items_per_page_change(self, e):
        """Handle items per page dropdown change"""
        self.screen.items_per_page = int(e.control.value)
        self.screen.current_page = 1
        self.update_table()

    def go_to_prev_page(self, e):
        """Go to previous page"""
        if self.screen.current_page > 1:
            self.screen.current_page -= 1
            self.update_table()

    def go_to_next_page(self, e):
        """Go to next page"""
        total_pages = self.get_total_pages()
        if self.screen.current_page < total_pages:
            self.screen.current_page += 1
            self.update_table()

    def get_total_pages(self):
        """Calculate total number of pages"""
        if not self.screen.filtered_students:
            return 1
        return max(
            1,
            (len(self.screen.filtered_students) + self.screen.items_per_page - 1)
            // self.screen.items_per_page,
        )

    def get_paginated_students(self):
        """Get students for current page"""
        start_idx = (self.screen.current_page - 1) * self.screen.items_per_page
        end_idx = start_idx + self.screen.items_per_page
        return self.screen.filtered_students[start_idx:end_idx]

    def apply_filters(self):
        """Apply search and filters to students data"""
        if not self.screen.students_data:
            self.screen.filtered_students = []
            return

        query = self.screen.search_query.lower().strip()

        # Start with all students
        filtered = self.screen.students_data.copy()

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
        if self.screen.selected_classroom_filter != "all":
            classroom_id = int(self.screen.selected_classroom_filter)
            # Get students enrolled in the selected classroom
            enrolled_student_ids = [
                enrollment.student_id
                for enrollment in self.screen.enrollments_data
                if enrollment.classroom_id == classroom_id
            ]
            filtered = [
                student
                for student in filtered
                if student.id_student in enrolled_student_ids
            ]

        # Apply gender filter
        if self.screen.selected_gender_filter != "all":
            filtered = [
                student
                for student in filtered
                if student.gender.lower()[0]
                == self.screen.selected_gender_filter.lower()[0]
            ]

        self.screen.filtered_students = filtered

    def update_classroom_filter_options(self):
        """Update classroom filter dropdown options"""
        if not hasattr(self.screen, "classroom_filter_dropdown"):
            return

        options = [
            DropdownOption(key="all", text=self.screen.get_text("all_classrooms")),
        ]

        for classroom in self.screen.classrooms_data:
            options.append(
                DropdownOption(key=str(classroom.id_classroom), text=classroom.name)
            )

        self.screen.classroom_filter_dropdown.options = options

    def get_classroom_name(self, student_id) -> str:
        """Get classroom name for a student"""
        for enrollment in self.screen.enrollments_data:
            if enrollment.student_id == student_id:
                for classroom in self.screen.classrooms_data:
                    if classroom.id_classroom == enrollment.classroom_id:
                        return classroom.name
        return "N/A"

    def get_birth_year(self, date_of_birth: str) -> str:
        """Extract birth year from date string"""
        try:
            # Assuming date format is YY-MM-DD
            parts = date_of_birth.replace("/", "-").split("-")
            if len(parts) == 3:
                return parts[0]  # Year is the first part
        except:
            pass
        return "N/A"
