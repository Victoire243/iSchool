"""
Admin Forms Module
Contains all form-related components and logic for the admin screen
"""

from flet import *  # type: ignore
from core import Constants


class AdminForms:
    """Manages all forms for admin entities"""

    def __init__(self, parent):
        """
        Initialize forms with reference to parent AdminScreen
        Args:
            parent: Reference to AdminScreen instance
        """
        self.parent = parent
        self._build_all_forms()

    def _build_all_forms(self):
        """Build all form components"""
        self._build_user_form()
        self._build_classroom_form()
        self._build_school_year_form()
        self._build_staff_form()

    def _build_user_form(self):
        """Build user form components"""
        self.parent.user_username_field = TextField(
            label=self.parent.get_text("username"),
            hint_text=self.parent.get_text("enter_username"),
            autofocus=True,
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            helper=self.parent.get_text("username_helper"),
        )

        self.parent.user_email_field = TextField(
            label=self.parent.get_text("email"),
            hint_text=self.parent.get_text("enter_email"),
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            helper=self.parent.get_text("email_helper"),
            keyboard_type=KeyboardType.EMAIL,
        )

        self.parent.user_password_field = TextField(
            label=self.parent.get_text("password"),
            hint_text=self.parent.get_text("enter_password"),
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            helper=self.parent.get_text("password_helper"),
            password=True,
            can_reveal_password=True,
        )

        self.parent.user_role_dropdown = Dropdown(
            label=self.parent.get_text("role"),
            border_radius=BorderRadius.all(5),
            options=[],
            expand=1,
            helper_text=self.parent.get_text("select_role"),
            width=float("inf"),
            menu_width=200,
        )

        self.parent.user_submit_button = Button(
            content=self.parent.get_text("submit"),
            icon=Icons.SAVE,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                bgcolor=Constants.PRIMARY_COLOR,
                padding=Padding(10, 20, 10, 20),
                color="white",
            ),
            on_click=self.parent._submit_user_form,
        )

        self.parent.user_cancel_button = Button(
            content=self.parent.get_text("cancel"),
            icon=Icons.CANCEL,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                bgcolor=Constants.CANCEL_COLOR,
                padding=Padding(10, 20, 10, 20),
                color="white",
            ),
            on_click=self.parent._close_form,
        )

        self.parent.user_form_container = Column(
            horizontal_alignment=CrossAxisAlignment.STRETCH,
            controls=[
                Text(
                    value=self.parent.get_text("add_user"),
                    style=TextStyle(
                        size=18,
                        weight=FontWeight.BOLD,
                        color=Constants.PRIMARY_COLOR,
                    ),
                ),
                Row(
                    controls=[
                        self.parent.user_username_field,
                        self.parent.user_email_field,
                    ],
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=CrossAxisAlignment.CENTER,
                ),
                Row(
                    controls=[
                        self.parent.user_password_field,
                        self.parent.user_role_dropdown,
                    ],
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=CrossAxisAlignment.CENTER,
                ),
                Row(
                    controls=[
                        self.parent.user_submit_button,
                        self.parent.user_cancel_button,
                    ],
                    alignment=MainAxisAlignment.END,
                ),
            ],
        )

    def _build_classroom_form(self):
        """Build classroom form components"""
        self.parent.classroom_name_field = TextField(
            label=self.parent.get_text("classroom_name"),
            hint_text=self.parent.get_text("enter_classroom_name"),
            autofocus=True,
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            helper=self.parent.get_text("classroom_name_helper"),
        )

        self.parent.classroom_level_field = TextField(
            label=self.parent.get_text("level"),
            hint_text=self.parent.get_text("enter_level"),
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            helper=self.parent.get_text("level_helper"),
        )

        self.parent.classroom_submit_button = Button(
            content=self.parent.get_text("submit"),
            icon=Icons.SAVE,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                bgcolor=Constants.PRIMARY_COLOR,
                padding=Padding(10, 20, 10, 20),
                color="white",
            ),
            on_click=self.parent._submit_classroom_form,
        )

        self.parent.classroom_cancel_button = Button(
            content=self.parent.get_text("cancel"),
            icon=Icons.CANCEL,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                bgcolor=Constants.CANCEL_COLOR,
                padding=Padding(10, 20, 10, 20),
                color="white",
            ),
            on_click=self.parent._close_form,
        )

        self.parent.classroom_form_container = Column(
            horizontal_alignment=CrossAxisAlignment.STRETCH,
            controls=[
                Text(
                    value=self.parent.get_text("add_classroom"),
                    style=TextStyle(
                        size=18,
                        weight=FontWeight.BOLD,
                        color=Constants.PRIMARY_COLOR,
                    ),
                ),
                Row(
                    controls=[
                        self.parent.classroom_name_field,
                        self.parent.classroom_level_field,
                    ],
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=CrossAxisAlignment.CENTER,
                ),
                Row(
                    controls=[
                        self.parent.classroom_submit_button,
                        self.parent.classroom_cancel_button,
                    ],
                    alignment=MainAxisAlignment.END,
                ),
            ],
        )

    def _build_school_year_form(self):
        """Build school year form components"""
        self.parent.school_year_name_field = TextField(
            label=self.parent.get_text("school_year_name"),
            hint_text=self.parent.get_text("enter_school_year_name"),
            autofocus=True,
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            helper=self.parent.get_text("school_year_name_helper"),
        )

        self.parent.school_year_start_date_field = TextField(
            label=self.parent.get_text("start_date"),
            hint_text=self.parent.get_text("enter_start_date"),
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            helper=self.parent.get_text("date_format_yyyy_mm_dd"),
            keyboard_type=KeyboardType.DATETIME,
            value="2024-09-01",
        )

        self.parent.school_year_end_date_field = TextField(
            label=self.parent.get_text("end_date"),
            hint_text=self.parent.get_text("enter_end_date"),
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            helper=self.parent.get_text("date_format_yyyy_mm_dd"),
            keyboard_type=KeyboardType.DATETIME,
            value="2025-06-30",
        )

        self.parent.school_year_status_switch = Switch(
            label=self.parent.get_text("active"),
            value=False,
        )

        self.parent.school_year_submit_button = Button(
            content=self.parent.get_text("submit"),
            icon=Icons.SAVE,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                bgcolor=Constants.PRIMARY_COLOR,
                padding=Padding(10, 20, 10, 20),
                color="white",
            ),
            on_click=self.parent._submit_school_year_form,
        )

        self.parent.school_year_cancel_button = Button(
            content=self.parent.get_text("cancel"),
            icon=Icons.CANCEL,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                bgcolor=Constants.CANCEL_COLOR,
                padding=Padding(10, 20, 10, 20),
                color="white",
            ),
            on_click=self.parent._close_form,
        )

        self.parent.school_year_form_container = Column(
            horizontal_alignment=CrossAxisAlignment.STRETCH,
            controls=[
                Text(
                    value=self.parent.get_text("add_school_year"),
                    style=TextStyle(
                        size=18,
                        weight=FontWeight.BOLD,
                        color=Constants.PRIMARY_COLOR,
                    ),
                ),
                Row(
                    controls=[
                        self.parent.school_year_name_field,
                        self.parent.school_year_start_date_field,
                        self.parent.school_year_end_date_field,
                    ],
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=CrossAxisAlignment.CENTER,
                ),
                Container(
                    content=self.parent.school_year_status_switch,
                    padding=Padding.symmetric(vertical=10),
                ),
                Row(
                    controls=[
                        self.parent.school_year_submit_button,
                        self.parent.school_year_cancel_button,
                    ],
                    alignment=MainAxisAlignment.END,
                ),
            ],
        )

    def _build_staff_form(self):
        """Build staff form components"""
        self.parent.staff_first_name_field = TextField(
            label=self.parent.get_text("first_name"),
            hint_text=self.parent.get_text("enter_first_name"),
            autofocus=True,
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            helper=self.parent.get_text("staff_first_name_helper"),
        )

        self.parent.staff_last_name_field = TextField(
            label=self.parent.get_text("last_name"),
            hint_text=self.parent.get_text("enter_last_name"),
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            helper=self.parent.get_text("staff_last_name_helper"),
        )

        self.parent.staff_position_field = TextField(
            label=self.parent.get_text("position"),
            hint_text=self.parent.get_text("enter_position"),
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            helper=self.parent.get_text("position_helper"),
        )

        self.parent.staff_hire_date_field = TextField(
            label=self.parent.get_text("hire_date"),
            hint_text=self.parent.get_text("enter_hire_date"),
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            helper=self.parent.get_text("hire_date_helper"),
            keyboard_type=KeyboardType.DATETIME,
            value="2024-01-01",
        )

        self.parent.staff_salary_field = TextField(
            label=self.parent.get_text("salary_base"),
            hint_text=self.parent.get_text("enter_salary"),
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            helper=self.parent.get_text("salary_helper"),
            keyboard_type=KeyboardType.NUMBER,
            input_filter=NumbersOnlyInputFilter(),
        )

        self.parent.staff_submit_button = Button(
            content=self.parent.get_text("submit"),
            icon=Icons.SAVE,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                bgcolor=Constants.PRIMARY_COLOR,
                padding=Padding(10, 20, 10, 20),
                color="white",
            ),
            on_click=self.parent._submit_staff_form,
        )

        self.parent.staff_cancel_button = Button(
            content=self.parent.get_text("cancel"),
            icon=Icons.CANCEL,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                bgcolor=Constants.CANCEL_COLOR,
                padding=Padding(10, 20, 10, 20),
                color="white",
            ),
            on_click=self.parent._close_form,
        )

        self.parent.staff_form_container = Column(
            horizontal_alignment=CrossAxisAlignment.STRETCH,
            controls=[
                Text(
                    value=self.parent.get_text("add_staff"),
                    style=TextStyle(
                        size=18,
                        weight=FontWeight.BOLD,
                        color=Constants.PRIMARY_COLOR,
                    ),
                ),
                Row(
                    controls=[
                        self.parent.staff_first_name_field,
                        self.parent.staff_last_name_field,
                        self.parent.staff_position_field,
                    ],
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=CrossAxisAlignment.CENTER,
                ),
                Row(
                    controls=[
                        self.parent.staff_hire_date_field,
                        self.parent.staff_salary_field,
                    ],
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=CrossAxisAlignment.CENTER,
                ),
                Row(
                    controls=[
                        self.parent.staff_submit_button,
                        self.parent.staff_cancel_button,
                    ],
                    alignment=MainAxisAlignment.END,
                ),
            ],
        )

    def clear_all_forms(self):
        """Clear all form fields"""
        # Clear user form
        if hasattr(self.parent, "user_username_field"):
            self.parent.user_username_field.value = ""
            self.parent.user_email_field.value = ""
            self.parent.user_password_field.value = ""
            self.parent.user_role_dropdown.value = None

        # Clear classroom form
        if hasattr(self.parent, "classroom_name_field"):
            self.parent.classroom_name_field.value = ""
            self.parent.classroom_level_field.value = ""

        # Clear school year form
        if hasattr(self.parent, "school_year_name_field"):
            self.parent.school_year_name_field.value = ""
            self.parent.school_year_start_date_field.value = "2024-09-01"
            self.parent.school_year_end_date_field.value = "2025-06-30"
            self.parent.school_year_status_switch.value = False

        # Clear staff form
        if hasattr(self.parent, "staff_first_name_field"):
            self.parent.staff_first_name_field.value = ""
            self.parent.staff_last_name_field.value = ""
            self.parent.staff_position_field.value = ""
            self.parent.staff_hire_date_field.value = "2024-01-01"
            self.parent.staff_salary_field.value = ""

    def populate_roles_dropdown(self):
        """Populate roles dropdown with available roles"""
        # TODO: Load roles from services
        # For now, using placeholder roles
        self.parent.user_role_dropdown.options = [
            DropdownOption(key="1", text="Administrateur"),
            DropdownOption(key="2", text="Enseignant"),
            DropdownOption(key="3", text="Comptable"),
            DropdownOption(key="4", text="Surveillant"),
        ]

    def populate_roles_dropdown_for_edit(self):
        """Populate roles dropdown for edit dialog"""
        self.parent.edit_user_role_dropdown.options = [
            DropdownOption(key="1", text="Administrateur"),
            DropdownOption(key="2", text="Enseignant"),
            DropdownOption(key="3", text="Comptable"),
            DropdownOption(key="4", text="Surveillant"),
        ]
