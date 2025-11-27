from flet import *
from core import Constants
from models import StudentModel
from .students_components import StudentsComponents
import asyncio


class StudentsDialogs:
    def __init__(self, students_screen):
        self.screen = students_screen

    def build_edit_dialog(self):
        """Build the edit student dialog"""
        # Create form fields for edit dialog
        self.screen.edit_first_name_field = TextField(
            label=self.screen.get_text("first_name"),
            hint_text=self.screen.get_text("enter_first_name"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
        )

        self.screen.edit_last_name_field = TextField(
            label=self.screen.get_text("last_name"),
            hint_text=self.screen.get_text("enter_last_name"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
        )

        self.screen.edit_surname_field = TextField(
            label=self.screen.get_text("surname"),
            hint_text=self.screen.get_text("enter_surname"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
        )

        self.screen.edit_birth_date_field = TextField(
            label=self.screen.get_text("birth_date"),
            hint_text=self.screen.get_text("enter_birth_date"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            keyboard_type=KeyboardType.DATETIME,
            expand=1,
        )

        self.screen.edit_gender_dropdown = Dropdown(
            label=self.screen.get_text("gender"),
            border_radius=BorderRadius.all(5),
            options=[
                DropdownOption(key="male", text=self.screen.get_text("male")),
                DropdownOption(key="female", text=self.screen.get_text("female")),
            ],
            expand=1,
            width=float("inf"),
            menu_width=150,
        )

        self.screen.edit_classroom_dropdown = Dropdown(
            label=self.screen.get_text("classroom"),
            border_radius=BorderRadius.all(5),
            options=[],
            expand=1,
            width=float("inf"),
            menu_width=250,
        )

        self.screen.edit_address_field = TextField(
            label=self.screen.get_text("address"),
            hint_text=self.screen.get_text("enter_address"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            multiline=True,
            min_lines=2,
            max_lines=3,
            expand=1,
        )

        self.screen.edit_parent_contact_field = TextField(
            label=self.screen.get_text("parent_contact"),
            hint_text=self.screen.get_text("enter_parent_contact"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            multiline=True,
            min_lines=2,
            max_lines=3,
            expand=1,
        )

        # Create the dialog
        self.screen.edit_dialog = AlertDialog(
            modal=True,
            scrollable=True,
            bgcolor="#f8faff",
            title=Container(
                content=Text(
                    self.screen.get_text("edit_student"),
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
                                self.screen.edit_first_name_field,
                                self.screen.edit_last_name_field,
                            ],
                            spacing=10,
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        Row(
                            controls=[
                                self.screen.edit_surname_field,
                                self.screen.edit_birth_date_field,
                            ],
                            spacing=10,
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        Row(
                            controls=[
                                self.screen.edit_gender_dropdown,
                                self.screen.edit_classroom_dropdown,
                            ],
                            spacing=10,
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        Row(
                            controls=[
                                self.screen.edit_address_field,
                                self.screen.edit_parent_contact_field,
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
                **StudentsComponents.get_box_style(),
            ),
            actions=[
                Button(
                    content=Text(self.screen.get_text("cancel")),
                    on_click=self.close_edit_dialog,
                    style=ButtonStyle(
                        shape=RoundedRectangleBorder(radius=5),
                        bgcolor=Constants.CANCEL_COLOR,
                        padding=Padding(10, 20, 10, 20),
                        color="white",
                    ),
                ),
                Button(
                    content=Text(self.screen.get_text("update")),
                    on_click=self.screen.form_handlers.save_student_changes,
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

    def build_delete_dialog(self):

        self.screen.motive_field = TextField(
            label=self.screen.get_text("motive"),
            hint_text=self.screen.get_text("enter_motive"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=True,
            multiline=True,
            min_lines=2,
            max_lines=5,
        )

        self.screen.student_name_to_be_deleted = Text(
            value="",
            weight=FontWeight.BOLD,
        )

        self.screen.delete_dialog = AlertDialog(
            modal=True,
            scrollable=True,
            bgcolor="#f8faff",
            title=Container(
                content=Text(
                    self.screen.get_text("delete_student"),
                    weight=FontWeight.BOLD,
                    color="white",
                ),
                padding=Padding.symmetric(horizontal=20, vertical=10),
                align=Alignment.CENTER_LEFT,
                alignment=Alignment.CENTER_LEFT,
                border_radius=BorderRadius.all(10),
                bgcolor=Constants.CANCEL_COLOR,
            ),
            content=Container(
                content=Column(
                    controls=[
                        Text(
                            self.screen.get_text("confirm_delete_student"),
                            size=14,
                            color=Constants.PRIMARY_COLOR,
                        ),
                        self.screen.student_name_to_be_deleted,
                        self.screen.motive_field,
                    ],
                    spacing=15,
                    tight=True,
                    horizontal_alignment=CrossAxisAlignment.STRETCH,
                ),
                width=400,
                padding=Padding.all(20),
                align=Alignment.CENTER_LEFT,
                alignment=Alignment.CENTER_LEFT,
                clip_behavior=ClipBehavior.HARD_EDGE,
                **StudentsComponents.get_box_style(),
            ),
            actions=[
                Button(
                    content=Text(self.screen.get_text("cancel")),
                    on_click=self.close_delete_dialog,
                    style=ButtonStyle(
                        shape=RoundedRectangleBorder(radius=5),
                        bgcolor=Constants.PRIMARY_COLOR,
                        padding=Padding(10, 20, 10, 20),
                        color="white",
                    ),
                ),
                Button(
                    content=Text(self.screen.get_text("delete")),
                    on_click=self.screen.form_handlers.confirm_delete_student,
                    style=ButtonStyle(
                        shape=RoundedRectangleBorder(radius=5),
                        bgcolor=Constants.CANCEL_COLOR,
                        padding=Padding(10, 20, 10, 20),
                        color="white",
                    ),
                ),
            ],
            actions_alignment=MainAxisAlignment.END,
        )

    def build_import_dialog(self):
        """Build the import students dialog"""

        # File path display
        self.screen.import_file_path_text = Text(
            value=self.screen.get_text("no_file_selected"),
            size=14,
            color=Colors.GREY_600,
            italic=True,
        )

        # File picker button
        self.screen.import_file_picker_button = Button(
            content=Text(self.screen.get_text("browse_file")),
            icon=Icons.FOLDER_OPEN,
            on_click=self.pick_import_file,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                bgcolor=Constants.PRIMARY_COLOR,
                padding=Padding(10, 20, 10, 20),
                color="white",
            ),
        )

        # File details container (hidden by default)
        self.screen.import_male_count_text = Text(
            value="0", size=20, weight=FontWeight.BOLD
        )
        self.screen.import_female_count_text = Text(
            value="0", size=20, weight=FontWeight.BOLD
        )
        self.screen.import_total_count_text = Text(
            value="0", size=20, weight=FontWeight.BOLD
        )

        self.screen.import_file_details_container = Container(
            content=Column(
                controls=[
                    Text(
                        self.screen.get_text("file_details"),
                        size=16,
                        weight=FontWeight.BOLD,
                        color=Constants.PRIMARY_COLOR,
                    ),
                    Divider(height=1, color=Constants.PRIMARY_COLOR),
                    Row(
                        controls=[
                            self.create_detail_stat(
                                self.screen.get_text("total_records"),
                                self.screen.import_total_count_text,
                                Icons.PEOPLE,
                                Constants.PRIMARY_COLOR,
                            ),
                            self.create_detail_stat(
                                self.screen.get_text("male_count"),
                                self.screen.import_male_count_text,
                                Icons.MALE,
                                Colors.BLUE,
                            ),
                            self.create_detail_stat(
                                self.screen.get_text("female_count"),
                                self.screen.import_female_count_text,
                                Icons.FEMALE,
                                Colors.PINK,
                            ),
                        ],
                        alignment=MainAxisAlignment.SPACE_AROUND,
                        spacing=10,
                    ),
                ],
                spacing=10,
            ),
            visible=False,
            padding=Padding.all(15),
            border_radius=BorderRadius.all(10),
            bgcolor="#e8f4f8",
            margin=Margin(top=10, bottom=10),
        )

        # Classroom dropdown for import
        self.screen.import_classroom_dropdown = Dropdown(
            label=self.screen.get_text("select_classroom_for_import"),
            border_radius=BorderRadius.all(5),
            options=[],
            helper_text=self.screen.get_text("classroom_required"),
            # width=float("inf"),
        )

        # Import button (disabled by default)
        self.screen.import_confirm_button = Button(
            content=Text(self.screen.get_text("import")),
            icon=Icons.UPLOAD,
            disabled=True,
            on_click=self.confirm_import,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                bgcolor=Constants.PRIMARY_COLOR,
                padding=Padding(10, 20, 10, 20),
                color="white",
            ),
        )

        # Create the dialog
        self.screen.import_dialog = AlertDialog(
            modal=True,
            scrollable=True,
            bgcolor="#f8faff",
            title=Container(
                content=Text(
                    self.screen.get_text("import_students"),
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
                        Text(
                            self.screen.get_text("select_file"),
                            size=14,
                            weight=FontWeight.BOLD,
                            color=Constants.PRIMARY_COLOR,
                        ),
                        Row(
                            controls=[
                                self.screen.import_file_path_text,
                                self.screen.import_file_picker_button,
                            ],
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=CrossAxisAlignment.CENTER,
                            spacing=10,
                        ),
                        self.screen.import_file_details_container,
                        self.screen.import_classroom_dropdown,
                    ],
                    spacing=15,
                    tight=True,
                    horizontal_alignment=CrossAxisAlignment.STRETCH,
                ),
                width=600,
                padding=Padding.all(20),
                align=Alignment.CENTER_LEFT,
                alignment=Alignment.CENTER_LEFT,
                clip_behavior=ClipBehavior.HARD_EDGE,
            ),
            actions=[
                Button(
                    content=Text(self.screen.get_text("cancel")),
                    on_click=self.close_import_dialog,
                    style=ButtonStyle(
                        shape=RoundedRectangleBorder(radius=5),
                        bgcolor=Constants.CANCEL_COLOR,
                        padding=Padding(10, 20, 10, 20),
                        color="white",
                    ),
                ),
                self.screen.import_confirm_button,
            ],
            actions_alignment=MainAxisAlignment.END,
        )

        # Store for parsed data
        self.screen.parsed_students = []
        self.screen.import_file_path = None

    def create_detail_stat(
        self, title: str, value_control: Control, icon: str, color: str
    ) -> Control:
        """Create a detail statistic card for import dialog"""
        return Container(
            content=Column(
                controls=[
                    Icon(icon, color=color, size=30),
                    Text(
                        title,
                        size=12,
                        color=Colors.GREY_600,
                        text_align=TextAlign.CENTER,
                    ),
                    value_control,
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=5,
            ),
            padding=Padding.all(10),
            expand=1,
            border_radius=BorderRadius.all(10),
            bgcolor="white",
            shadow=BoxShadow(color="black12", blur_radius=3, offset=Offset(0, 1)),
        )

    async def pick_import_file(self, e):
        """Open file picker to select CSV or Excel file"""
        import os

        def on_file_picked(result: list[FilePickerFile]):
            if result:
                file_path = result[0].path
                self.screen.import_file_path = file_path
                self.screen.import_file_path_text.value = os.path.basename(file_path)
                self.screen.import_file_path_text.italic = False
                self.screen.import_file_path_text.color = Constants.PRIMARY_COLOR

                # Parse the file
                asyncio.create_task(self.parse_import_file(file_path))

                self.screen.import_file_path_text.update()

        file_picker = FilePicker()
        # self.screen.page.overlay.append(file_picker)
        # self.screen.page.update()

        result = await file_picker.pick_files(
            allowed_extensions=["csv", "xlsx", "xls"],
            file_type=FilePickerFileType.CUSTOM,
            dialog_title=self.screen.get_text("select_file"),
        )
        on_file_picked(result)

    async def parse_import_file(self, file_path: str):
        """Parse CSV or Excel file and extract student data"""
        import os

        try:
            file_extension = os.path.splitext(file_path)[1].lower()

            if file_extension == ".csv":
                students = await self.parse_csv_file(file_path)
            elif file_extension in [".xlsx", ".xls"]:
                students = await self.parse_excel_file(file_path)
            else:
                self.screen.show_error_snackbar(
                    self.screen.get_text("invalid_file_format")
                )
                return

            if students:
                self.screen.parsed_students = students

                # Calculate statistics
                male_count = sum(
                    1 for s in students if s.gender.upper().startswith("M")
                )
                female_count = sum(
                    1 for s in students if s.gender.upper().startswith("F")
                )
                total_count = len(students)

                # Update UI
                self.screen.import_male_count_text.value = str(male_count)
                self.screen.import_female_count_text.value = str(female_count)
                self.screen.import_total_count_text.value = str(total_count)
                self.screen.import_file_details_container.visible = True
                self.screen.import_confirm_button.disabled = False

                # Update classroom dropdown
                self.populate_import_classroom_dropdown()

                try:
                    self.screen.import_male_count_text.update()
                    self.screen.import_female_count_text.update()
                    self.screen.import_total_count_text.update()
                    self.screen.import_file_details_container.update()
                    self.screen.import_confirm_button.update()
                    self.screen.import_classroom_dropdown.update()
                except:
                    pass
            else:
                self.screen.show_error_snackbar(
                    self.screen.get_text("file_format_error")
                )

        except Exception as ex:
            print(f"Error parsing file: {ex}")
            self.screen.show_error_snackbar(
                f"{self.screen.get_text('import_error')}: {str(ex)}"
            )

    async def parse_csv_file(self, file_path: str) -> list:
        """Parse CSV file and return list of StudentModel objects"""
        import csv

        students = []

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    try:
                        student = StudentModel(
                            id_student=0,  # Will be assigned by database
                            first_name=row.get("first_name", "").strip(),
                            last_name=row.get("last_name", "").strip(),
                            surname=row.get("surname", "").strip(),
                            gender=row.get("gender", "M").strip().upper(),
                            date_of_birth=row.get(
                                "date_of_birth", "01-01-2000"
                            ).strip(),
                            address=row.get("address", "").strip(),
                            parent_contact=row.get("parent_contact", "").strip(),
                        )
                        students.append(student)
                    except Exception as e:
                        print(f"Error parsing row: {e}")
                        continue
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            raise

        return students

    async def parse_excel_file(self, file_path: str) -> list:
        """Parse Excel file and return list of StudentModel objects"""
        try:
            import openpyxl
        except ImportError:
            self.screen.show_error_snackbar(
                "openpyxl library not installed. Please install it to import Excel files."
            )
            return []

        students = []

        try:
            workbook = openpyxl.load_workbook(file_path)
            sheet = workbook.active

            # Assume first row is header
            headers = [cell.value for cell in sheet[1]]

            # Find column indices
            first_name_idx = (
                headers.index("first_name") if "first_name" in headers else 0
            )
            last_name_idx = headers.index("last_name") if "last_name" in headers else 1
            surname_idx = headers.index("surname") if "surname" in headers else 2
            gender_idx = headers.index("gender") if "gender" in headers else 3
            date_of_birth_idx = (
                headers.index("date_of_birth") if "date_of_birth" in headers else 4
            )
            address_idx = headers.index("address") if "address" in headers else 5
            parent_contact_idx = (
                headers.index("parent_contact") if "parent_contact" in headers else 6
            )

            # Read rows (skip header)
            for row in sheet.iter_rows(min_row=2, values_only=True):
                try:
                    student = StudentModel(
                        id_student=0,  # Will be assigned by database
                        first_name=str(row[first_name_idx] or "").strip(),
                        last_name=str(row[last_name_idx] or "").strip(),
                        surname=str(row[surname_idx] or "").strip(),
                        gender=str(row[gender_idx] or "M").strip().upper(),
                        date_of_birth=str(
                            row[date_of_birth_idx] or "01-01-2000"
                        ).strip(),
                        address=str(row[address_idx] or "").strip(),
                        parent_contact=str(row[parent_contact_idx] or "").strip(),
                    )
                    students.append(student)
                except Exception as e:
                    print(f"Error parsing row: {e}")
                    continue

            workbook.close()
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            raise

        return students

    def populate_import_classroom_dropdown(self):
        """Populate classroom dropdown for import"""
        if self.screen.classrooms_data:
            options = [
                DropdownOption(key=str(c.id_classroom), text=c.name)
                for c in self.screen.classrooms_data
            ]
            self.screen.import_classroom_dropdown.options = options
            if options:
                self.screen.import_classroom_dropdown.value = options[0].key

    def open_import_dialog(self, e):
        """Open the import dialog"""
        # Reset dialog state
        self.screen.import_file_path = None
        self.screen.parsed_students = []
        self.screen.import_file_path_text.value = self.screen.get_text(
            "no_file_selected"
        )
        self.screen.import_file_path_text.italic = True
        self.screen.import_file_path_text.color = Colors.GREY_600
        self.screen.import_file_details_container.visible = False
        self.screen.import_confirm_button.disabled = True

        # Populate classroom dropdown
        self.populate_import_classroom_dropdown()

        # Show dialog
        self.screen.page.show_dialog(self.screen.import_dialog)
        self.screen.page.update()

    def close_import_dialog(self, e=None):
        """Close the import dialog"""
        self.screen.import_dialog.open = False
        self.screen.page.update()

    async def confirm_import(self, e):
        """Confirm and execute import"""
        if not self.screen.parsed_students:
            self.screen.show_error_snackbar(self.screen.get_text("no_file_selected"))
            return

        if not self.screen.import_classroom_dropdown.value:
            self.screen.show_error_snackbar(self.screen.get_text("classroom_required"))
            return

        try:
            classroom_id = int(self.screen.import_classroom_dropdown.value)

            # Disable button and show processing
            self.screen.import_confirm_button.disabled = True
            self.screen.import_confirm_button.content = Text(
                self.screen.get_text("processing_file")
            )
            self.screen.import_confirm_button.update()

            # Call service to import
            success, imported_count = await self.screen.services.import_students(
                self.screen.parsed_students, classroom_id
            )

            if success:
                self.close_import_dialog()
                # self.screen.show_success_snackbar(
                #     f"{imported_count} {self.screen.get_text('students_imported')}"
                # )
                # Reload data
                await self.screen.load_data()
            else:
                self.screen.show_error_snackbar(self.screen.get_text("import_error"))
                self.screen.import_confirm_button.disabled = False
                self.screen.import_confirm_button.content = Text(
                    self.screen.get_text("import")
                )
                self.screen.import_confirm_button.update()

        except Exception as ex:
            print(f"Error during import: {ex}")
            # self.screen.show_error_snackbar(
            #     f"{self.screen.get_text('import_error')}: {str(ex)}"
            # )
            self.screen.import_confirm_button.disabled = False
            self.screen.import_confirm_button.content = Text(
                self.screen.get_text("import")
            )
            self.screen.import_confirm_button.update()

    def open_edit_dialog(self, student: StudentModel):
        """Open edit dialog and populate with student data"""
        if not student:
            return

        # Store the current student being edited
        self.screen.current_editing_student_id = student.id_student

        # Populate form fields
        self.screen.edit_first_name_field.value = student.first_name
        self.screen.edit_last_name_field.value = student.last_name
        self.screen.edit_surname_field.value = student.surname
        self.screen.edit_birth_date_field.value = student.date_of_birth
        self.screen.edit_gender_dropdown.value = student.gender.lower()
        self.screen.edit_gender_dropdown.text = student.gender
        self.screen.edit_address_field.value = student.address
        self.screen.edit_parent_contact_field.value = student.parent_contact

        # Populate classroom dropdown
        classroom_options = [
            DropdownOption(key=str(c.id_classroom), text=c.name)
            for c in self.screen.classrooms_data
        ]
        self.screen.edit_classroom_dropdown.options = classroom_options

        # Find and set the current classroom
        current_classroom_id = None
        for enrollment in self.screen.enrollments_data:
            if enrollment.student_id == student.id_student:
                current_classroom_id = enrollment.classroom_id
                break

        if current_classroom_id:
            self.screen.edit_classroom_dropdown.value = str(current_classroom_id)

        # Open the dialog
        self.screen.page.show_dialog(self.screen.edit_dialog)

    def open_delete_dialog(self, student: StudentModel):
        """Open delete dialog and populate with student data"""
        if not student:
            return

        # Store the current student being deleted
        self.screen.current_deleting_student_id = student.id_student

        # Set the student name in the dialog
        full_name = f"{student.last_name} {student.surname} {student.first_name}"
        self.screen.student_name_to_be_deleted.value = full_name

        # Clear motive field
        self.screen.motive_field.value = ""

        # Open the dialog
        self.screen.page.show_dialog(self.screen.delete_dialog)

    def close_dialog(self, e=None):
        self.screen.page.pop_dialog()

    def close_edit_dialog(self, e=None):
        """Close the edit dialog"""
        self.screen.edit_dialog.open = False
        self.screen.page.update()

    def close_delete_dialog(self, e=None):
        """Close the delete dialog"""
        self.screen.delete_dialog.open = False
        self.screen.page.update()

    def show_student_details_dialog(self, student: StudentModel):
        """Show student details dialog (TODO)"""

        dialog_content = Column(
            controls=[
                Text(
                    f"{self.screen.get_text('student')}: {student.first_name} {student.last_name} {student.surname}",
                    size=14,
                ),
                Divider(height=1),
                Text(
                    f"{self.screen.get_text('gender')}: {student.gender}",
                    size=14,
                ),
                Divider(height=1),
                Text(
                    f"{self.screen.get_text('birth_date')}: {student.date_of_birth}",
                    size=14,
                ),
                Divider(height=1),
                Text(
                    f"{self.screen.get_text('address')}: {student.address}",
                    size=14,
                ),
                Divider(height=1),
                Text(
                    f"{self.screen.get_text('parent_contact')}: {student.parent_contact}",
                    size=14,
                ),
            ],
            spacing=10,
        )

        dialog = AlertDialog(
            title=Text(self.screen.get_text("student_details"), weight=FontWeight.BOLD),
            content=dialog_content,
            actions=[
                TextButton(
                    content=self.screen.get_text("close"),
                    icon=Icons.CLOSE,
                    on_click=self.close_dialog,
                ),
            ],
            scrollable=True,
        )

        self.screen.page.show_dialog(dialog)
