from flet import *  # type: ignore
import asyncio
from core import AppState, Constants
from utils import Utils
from .admin_services import AdminServices
from models import UserModel, ClassroomModel, SchoolYearModel, StaffModel


class AdminScreen:

    def __init__(self, app_state: AppState, page: Page):
        self.app_state = app_state
        self.page = page
        self.services = AdminServices(app_state)

        self.build_components()
        self._build_table_components()
        self._build_form_components()
        self._build_edit_dialogs()

    async def on_mount(self):
        """Called when the screen is mounted"""
        await self.load_data()

    def refresh_admin_data(self, e):
        """Refresh all payment data"""
        self.main_content.content = self.loading_indicator
        self.main_content.update()
        asyncio.create_task(self.load_data())

    def get_text(self, key: str) -> str:
        return self.app_state.translations.get(key, key)

    @staticmethod
    def get_box_style() -> dict:
        return {
            "border_radius": BorderRadius.all(10),
            "shadow": BoxShadow(color="black12", blur_radius=5, offset=Offset(0, 2)),
            "bgcolor": "#f8faff",
        }

    @staticmethod
    def get_color_by_user_role(role: str) -> ColorValue:
        if not role.strip():
            return Colors.GREEN
        match role.lower()[0]:
            case "a":  # Admin
                return Colors.RED
            case "c":  # Comptable
                return Colors.ORANGE
            case "e":  # Enseignant
                return Constants.PRIMARY_COLOR
            case "s":  # Surveillant
                return Constants.SECONDARY_COLOR
        return Colors.ORANGE

    async def load_data(self):
        """Load all necessary data for the admin screen"""
        try:
            # Load data in parallel
            (
                (users_status, users_data),
                (classrooms_status, classrooms_data),
                (staff_status, staff_data),
                (school_year_status, school_year_data),
            ) = await asyncio.gather(
                self.services.load_users_data(),
                self.services.load_classrooms_data(),
                self.services.load_staff_data(),
                self.services.load_school_years_data(),
                return_exceptions=True,
            )

            # Store data
            self.users_data = users_data if users_status else []
            self.classrooms_data = classrooms_data if classrooms_status else []
            self.staff_data = staff_data if staff_status else []
            self.school_year_data = school_year_data if school_year_status else []

            # Calculate statistics
            total_users = len(self.users_data)
            total_classrooms = len(self.classrooms_data)
            total_staff = len(self.staff_data)

            # Update main content with stats and table
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
                                title=self.get_text("total_users"),
                                value=str(total_users),
                                icon=Icons.PEOPLE,
                                color=Constants.PRIMARY_COLOR,
                            ),
                            self.create_stat_card(
                                title=self.get_text("total_classrooms"),
                                value=str(total_classrooms),
                                icon=Icons.CLASS_,
                                color=Constants.SECONDARY_COLOR,
                            ),
                            self.create_stat_card(
                                title=self.get_text("total_staff"),
                                value=str(total_staff),
                                icon=Icons.PERSON_4,
                                color=Colors.ORANGE,
                            ),
                        ],
                    ),
                    Container(
                        content=Row(
                            [self.active_menu, self.add_action_button],
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        margin=Margin(top=20, bottom=10),
                    ),
                    self.add_container,
                    self.data_table_container,
                ],
            )
            # await self._update_user_table()
            match self.active_menu.value:
                case "classrooms":
                    await self._update_classroom_table()
                case "users":
                    await self._update_user_table()
                case "school_years":
                    await self._update_school_year_table()
                case "staff":
                    await self._update_staff_table()
            try:
                self.main_content.update()
            except Exception as e:
                print(f"Erreur lors de la mise à jour de l'interface: {e}")
        except Exception as e:
            print(f"Erreur lors du chargement des données: {e}")
            self.main_content.content = Text(f"Erreur: {e}")
            if hasattr(self.main_content, "update"):
                self.main_content.update()

    def build_components(self):
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

        self.add_container = Container(
            padding=Padding.all(15),
            margin=Margin(top=10, bottom=10),
            expand=False,
            visible=False,
            clip_behavior=ClipBehavior.ANTI_ALIAS,
            **self.get_box_style(),
        )

        self.active_menu = Dropdown(
            value="users",
            text_style=TextStyle(
                size=18, color=Constants.PRIMARY_COLOR, weight=FontWeight.BOLD
            ),
            options=[
                DropdownOption(
                    key="users",
                    text=self.get_text("users_management"),
                    leading_icon=Icons.PEOPLE,
                    data="users",
                ),
                DropdownOption(
                    key="classrooms",
                    text=self.get_text("classrooms_management"),
                    leading_icon=Icons.CLASS_,
                    data="classrooms",
                ),
                DropdownOption(
                    key="school_years",
                    text=self.get_text("school_years_management"),
                    leading_icon=Icons.CALENDAR_MONTH,
                    data="school_years",
                ),
                DropdownOption(
                    key="staff",
                    text=self.get_text("staff_management"),
                    leading_icon=Icons.PERSON,
                    data="staff",
                ),
            ],
            dense=True,
            on_change=self._handle_active_menu_change,
        )
        self.add_action_button = Button(
            icon=Icons.ADD,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                bgcolor=Constants.PRIMARY_COLOR,
                padding=Padding(10, 20, 10, 20),
                color="white",
            ),
            on_click=self._open_form,
        )

    async def _handle_active_menu_change(self, e: Event):
        match e.control.value:
            case "classrooms":
                await self._update_classroom_table()
            case "users":
                await self._update_user_table()
            case "school_years":
                await self._update_school_year_table()
            case "staff":
                await self._update_staff_table()

        try:
            self.add_action_button.update()
            self.data_table_container.update()
        except Exception as ex:
            pass

    def _build_table_components(self):
        self.data_table_container = Container(
            content=Column(
                controls=[],
                scroll=ScrollMode.AUTO,
            ),
            padding=Padding.all(10),
            **self.get_box_style(),
        )

    #################################################################
    # ----------------------  FORMS --------------------------------#

    def _build_form_components(self):
        """Build all form components"""
        self._build_user_form()
        self._build_classroom_form()
        self._build_school_year_form()
        self._build_staff_form()

    def _build_user_form(self):
        """Build user form components"""
        self.user_username_field = TextField(
            label=self.get_text("username"),
            hint_text=self.get_text("enter_username"),
            autofocus=True,
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            helper=self.get_text("username_helper"),
        )

        self.user_email_field = TextField(
            label=self.get_text("email"),
            hint_text=self.get_text("enter_email"),
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            helper=self.get_text("email_helper"),
            keyboard_type=KeyboardType.EMAIL,
        )

        self.user_password_field = TextField(
            label=self.get_text("password"),
            hint_text=self.get_text("enter_password"),
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            helper=self.get_text("password_helper"),
            password=True,
            can_reveal_password=True,
        )

        self.user_role_dropdown = Dropdown(
            label=self.get_text("role"),
            border_radius=BorderRadius.all(5),
            options=[],
            expand=1,
            helper_text=self.get_text("select_role"),
            width=float("inf"),
            menu_width=200,
        )

        self.user_submit_button = Button(
            content=self.get_text("submit"),
            icon=Icons.SAVE,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                bgcolor=Constants.PRIMARY_COLOR,
                padding=Padding(10, 20, 10, 20),
                color="white",
            ),
            on_click=self._submit_user_form,
        )

        self.user_cancel_button = Button(
            content=self.get_text("cancel"),
            icon=Icons.CANCEL,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                bgcolor=Constants.CANCEL_COLOR,
                padding=Padding(10, 20, 10, 20),
                color="white",
            ),
            on_click=self._close_form,
        )

        self.user_form_container = Column(
            horizontal_alignment=CrossAxisAlignment.STRETCH,
            controls=[
                Text(
                    value=self.get_text("add_user"),
                    style=TextStyle(
                        size=18,
                        weight=FontWeight.BOLD,
                        color=Constants.PRIMARY_COLOR,
                    ),
                ),
                Row(
                    controls=[
                        self.user_username_field,
                        self.user_email_field,
                    ],
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=CrossAxisAlignment.CENTER,
                ),
                Row(
                    controls=[
                        self.user_password_field,
                        self.user_role_dropdown,
                    ],
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=CrossAxisAlignment.CENTER,
                ),
                Row(
                    controls=[
                        self.user_submit_button,
                        self.user_cancel_button,
                    ],
                    alignment=MainAxisAlignment.END,
                ),
            ],
        )

    def _build_classroom_form(self):
        """Build classroom form components"""
        self.classroom_name_field = TextField(
            label=self.get_text("classroom_name"),
            hint_text=self.get_text("enter_classroom_name"),
            autofocus=True,
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            helper=self.get_text("classroom_name_helper"),
        )

        self.classroom_level_field = TextField(
            label=self.get_text("level"),
            hint_text=self.get_text("enter_level"),
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            helper=self.get_text("level_helper"),
        )

        self.classroom_submit_button = Button(
            content=self.get_text("submit"),
            icon=Icons.SAVE,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                bgcolor=Constants.PRIMARY_COLOR,
                padding=Padding(10, 20, 10, 20),
                color="white",
            ),
            on_click=self._submit_classroom_form,
        )

        self.classroom_cancel_button = Button(
            content=self.get_text("cancel"),
            icon=Icons.CANCEL,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                bgcolor=Constants.CANCEL_COLOR,
                padding=Padding(10, 20, 10, 20),
                color="white",
            ),
            on_click=self._close_form,
        )

        self.classroom_form_container = Column(
            horizontal_alignment=CrossAxisAlignment.STRETCH,
            controls=[
                Text(
                    value=self.get_text("add_classroom"),
                    style=TextStyle(
                        size=18,
                        weight=FontWeight.BOLD,
                        color=Constants.PRIMARY_COLOR,
                    ),
                ),
                Row(
                    controls=[
                        self.classroom_name_field,
                        self.classroom_level_field,
                    ],
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=CrossAxisAlignment.CENTER,
                ),
                Row(
                    controls=[
                        self.classroom_submit_button,
                        self.classroom_cancel_button,
                    ],
                    alignment=MainAxisAlignment.END,
                ),
            ],
        )

    def _build_school_year_form(self):
        """Build school year form components"""
        self.school_year_name_field = TextField(
            label=self.get_text("school_year_name"),
            hint_text=self.get_text("enter_school_year_name"),
            autofocus=True,
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            helper=self.get_text("school_year_name_helper"),
        )

        self.school_year_start_date_field = TextField(
            label=self.get_text("start_date"),
            hint_text=self.get_text("enter_start_date"),
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            helper=self.get_text("date_format_yyyy_mm_dd"),
            keyboard_type=KeyboardType.DATETIME,
            value="2024-09-01",
        )

        self.school_year_end_date_field = TextField(
            label=self.get_text("end_date"),
            hint_text=self.get_text("enter_end_date"),
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            helper=self.get_text("date_format_yyyy_mm_dd"),
            keyboard_type=KeyboardType.DATETIME,
            value="2025-06-30",
        )

        self.school_year_status_switch = Switch(
            label=self.get_text("active"),
            value=False,
        )

        self.school_year_submit_button = Button(
            content=self.get_text("submit"),
            icon=Icons.SAVE,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                bgcolor=Constants.PRIMARY_COLOR,
                padding=Padding(10, 20, 10, 20),
                color="white",
            ),
            on_click=self._submit_school_year_form,
        )

        self.school_year_cancel_button = Button(
            content=self.get_text("cancel"),
            icon=Icons.CANCEL,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                bgcolor=Constants.CANCEL_COLOR,
                padding=Padding(10, 20, 10, 20),
                color="white",
            ),
            on_click=self._close_form,
        )

        self.school_year_form_container = Column(
            horizontal_alignment=CrossAxisAlignment.STRETCH,
            controls=[
                Text(
                    value=self.get_text("add_school_year"),
                    style=TextStyle(
                        size=18,
                        weight=FontWeight.BOLD,
                        color=Constants.PRIMARY_COLOR,
                    ),
                ),
                Row(
                    controls=[
                        self.school_year_name_field,
                        self.school_year_start_date_field,
                        self.school_year_end_date_field,
                    ],
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=CrossAxisAlignment.CENTER,
                ),
                Container(
                    content=self.school_year_status_switch,
                    padding=Padding.symmetric(vertical=10),
                ),
                Row(
                    controls=[
                        self.school_year_submit_button,
                        self.school_year_cancel_button,
                    ],
                    alignment=MainAxisAlignment.END,
                ),
            ],
        )

    def _build_staff_form(self):
        """Build staff form components"""
        self.staff_first_name_field = TextField(
            label=self.get_text("first_name"),
            hint_text=self.get_text("enter_first_name"),
            autofocus=True,
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            helper=self.get_text("staff_first_name_helper"),
        )

        self.staff_last_name_field = TextField(
            label=self.get_text("last_name"),
            hint_text=self.get_text("enter_last_name"),
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            helper=self.get_text("staff_last_name_helper"),
        )

        self.staff_position_field = TextField(
            label=self.get_text("position"),
            hint_text=self.get_text("enter_position"),
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            helper=self.get_text("position_helper"),
        )

        self.staff_hire_date_field = TextField(
            label=self.get_text("hire_date"),
            hint_text=self.get_text("enter_hire_date"),
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            helper=self.get_text("hire_date_helper"),
            keyboard_type=KeyboardType.DATETIME,
            value="2024-01-01",
        )

        self.staff_salary_field = TextField(
            label=self.get_text("salary_base"),
            hint_text=self.get_text("enter_salary"),
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            helper=self.get_text("salary_helper"),
            keyboard_type=KeyboardType.NUMBER,
            input_filter=NumbersOnlyInputFilter(),
        )

        self.staff_submit_button = Button(
            content=self.get_text("submit"),
            icon=Icons.SAVE,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                bgcolor=Constants.PRIMARY_COLOR,
                padding=Padding(10, 20, 10, 20),
                color="white",
            ),
            on_click=self._submit_staff_form,
        )

        self.staff_cancel_button = Button(
            content=self.get_text("cancel"),
            icon=Icons.CANCEL,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                bgcolor=Constants.CANCEL_COLOR,
                padding=Padding(10, 20, 10, 20),
                color="white",
            ),
            on_click=self._close_form,
        )

        self.staff_form_container = Column(
            horizontal_alignment=CrossAxisAlignment.STRETCH,
            controls=[
                Text(
                    value=self.get_text("add_staff"),
                    style=TextStyle(
                        size=18,
                        weight=FontWeight.BOLD,
                        color=Constants.PRIMARY_COLOR,
                    ),
                ),
                Row(
                    controls=[
                        self.staff_first_name_field,
                        self.staff_last_name_field,
                        self.staff_position_field,
                    ],
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=CrossAxisAlignment.CENTER,
                ),
                Row(
                    controls=[
                        self.staff_hire_date_field,
                        self.staff_salary_field,
                    ],
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=CrossAxisAlignment.CENTER,
                ),
                Row(
                    controls=[
                        self.staff_submit_button,
                        self.staff_cancel_button,
                    ],
                    alignment=MainAxisAlignment.END,
                ),
            ],
        )

    # Form management methods
    def _open_form(self, e):
        """Open the appropriate form based on active menu"""
        active_menu = self.active_menu.value

        # Set the appropriate form in add_container
        if active_menu == "users":
            self.add_container.content = self.user_form_container
            self._populate_roles_dropdown()
        elif active_menu == "classrooms":
            self.add_container.content = self.classroom_form_container
        elif active_menu == "school_years":
            self.add_container.content = self.school_year_form_container
        elif active_menu == "staff":
            self.add_container.content = self.staff_form_container

        # Show container and update button
        self.add_container.visible = True
        self.add_action_button.icon = Icons.CLOSE
        self.add_action_button.style.bgcolor = Constants.CANCEL_COLOR
        self.add_action_button.on_click = self._close_form

        self.add_container.update()
        self.add_action_button.update()

    def _close_form(self, e):
        """Close the form"""
        self.add_container.visible = False
        self.add_action_button.icon = Icons.ADD
        self.add_action_button.style.bgcolor = Constants.PRIMARY_COLOR
        self.add_action_button.on_click = self._open_form

        self._clear_forms()

        self.add_container.update()
        self.add_action_button.update()

    def _clear_forms(self):
        """Clear all form fields"""
        # Clear user form
        if hasattr(self, "user_username_field"):
            self.user_username_field.value = ""
            self.user_email_field.value = ""
            self.user_password_field.value = ""
            self.user_role_dropdown.value = None

        # Clear classroom form
        if hasattr(self, "classroom_name_field"):
            self.classroom_name_field.value = ""
            self.classroom_level_field.value = ""

        # Clear school year form
        if hasattr(self, "school_year_name_field"):
            self.school_year_name_field.value = ""
            self.school_year_start_date_field.value = "2024-09-01"
            self.school_year_end_date_field.value = "2025-06-30"
            self.school_year_status_switch.value = False

        # Clear staff form
        if hasattr(self, "staff_first_name_field"):
            self.staff_first_name_field.value = ""
            self.staff_last_name_field.value = ""
            self.staff_position_field.value = ""
            self.staff_hire_date_field.value = "2024-01-01"
            self.staff_salary_field.value = ""

    def _populate_roles_dropdown(self):
        """Populate roles dropdown with available roles"""
        # TODO: Load roles from services
        # For now, using placeholder roles
        self.user_role_dropdown.options = [
            DropdownOption(key="1", text="Administrateur"),
            DropdownOption(key="2", text="Enseignant"),
            DropdownOption(key="3", text="Comptable"),
            DropdownOption(key="4", text="Surveillant"),
        ]
        # if hasattr(self.user_role_dropdown, "update"):
        #     self.user_role_dropdown.update()

    # Form submission methods
    async def _submit_user_form(self, e):
        """Submit user form"""
        # Validate fields
        if not self.user_username_field.value:
            return

        if not self.user_email_field.value:
            return

        if not self.user_password_field.value:
            return

        if not self.user_role_dropdown.value:
            return

        # Create user data
        user_data = {
            "username": self.user_username_field.value,
            "email": self.user_email_field.value,
            "password": self.user_password_field.value,
            "role_id": int(self.user_role_dropdown.value),
        }

        # TODO: Submit to service
        print(f"User data to submit: {user_data}")

        # Close form and refresh data
        self._close_form(e)
        await self.load_data()

    async def _submit_classroom_form(self, e):
        """Submit classroom form"""
        # Validate fields
        if not self.classroom_name_field.value:
            return

        if not self.classroom_level_field.value:
            return

        # Create classroom data
        classroom_data = {
            "name": self.classroom_name_field.value,
            "level": self.classroom_level_field.value,
        }

        # TODO: Submit to service
        print(f"Classroom data to submit: {classroom_data}")

        # Close form and refresh data
        self._close_form(e)
        await self.load_data()

    async def _submit_school_year_form(self, e):
        """Submit school year form"""
        # Validate fields
        if not self.school_year_name_field.value:
            return

        # Create school year data
        school_year_data = {
            "name": self.school_year_name_field.value,
            "start_date": self.school_year_start_date_field.value,
            "end_date": self.school_year_end_date_field.value,
            "is_active": self.school_year_status_switch.value,
        }

        # TODO: Submit to service
        print(f"School year data to submit: {school_year_data}")

        # Close form and refresh data
        self._close_form(e)
        await self.load_data()

    async def _submit_staff_form(self, e):
        """Submit staff form"""
        # Validate fields
        if not self.staff_first_name_field.value:
            return

        if not self.staff_last_name_field.value:
            return

        if not self.staff_position_field.value:
            return

        if not self.staff_salary_field.value:
            return

        # Create staff data
        staff_data = {
            "first_name": self.staff_first_name_field.value,
            "last_name": self.staff_last_name_field.value,
            "position": self.staff_position_field.value,
            "hire_date": self.staff_hire_date_field.value,
            "salary_base": float(self.staff_salary_field.value),
        }

        # TODO: Submit to service
        print(f"Staff data to submit: {staff_data}")

        # Close form and refresh data
        self._close_form(e)
        await self.load_data()

    #################################################################
    # ----------------------  EDIT DIALOGS -------------------------#

    def _build_edit_dialogs(self):
        """Build all edit dialogs"""
        self._build_user_edit_dialog()
        self._build_classroom_edit_dialog()
        self._build_school_year_edit_dialog()
        self._build_staff_edit_dialog()
        self._build_delete_dialogs()

    def _build_user_edit_dialog(self):
        """Build user edit dialog"""
        self.edit_user_username_field = TextField(
            label=self.get_text("username"),
            hint_text=self.get_text("enter_username"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
        )

        self.edit_user_email_field = TextField(
            label=self.get_text("email"),
            hint_text=self.get_text("enter_email"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            keyboard_type=KeyboardType.EMAIL,
        )

        self.edit_user_password_field = TextField(
            label=self.get_text("password"),
            hint_text=self.get_text("enter_password"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            password=True,
            can_reveal_password=True,
        )

        self.edit_user_role_dropdown = Dropdown(
            label=self.get_text("role"),
            border_radius=BorderRadius.all(5),
            options=[],
            expand=1,
            width=float("inf"),
            menu_width=200,
        )

        self.edit_user_dialog = AlertDialog(
            modal=True,
            scrollable=True,
            bgcolor="#f8faff",
            title=Container(
                content=Text(
                    self.get_text("edit_user"),
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
                                self.edit_user_username_field,
                                self.edit_user_email_field,
                            ],
                            spacing=10,
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        Row(
                            controls=[
                                self.edit_user_password_field,
                                self.edit_user_role_dropdown,
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
                    on_click=self._close_user_edit_dialog,
                    style=ButtonStyle(
                        shape=RoundedRectangleBorder(radius=5),
                        bgcolor=Constants.CANCEL_COLOR,
                        padding=Padding(10, 20, 10, 20),
                        color="white",
                    ),
                ),
                Button(
                    content=Text(self.get_text("update")),
                    on_click=self._save_user_changes,
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

    def _build_classroom_edit_dialog(self):
        """Build classroom edit dialog"""
        self.edit_classroom_name_field = TextField(
            label=self.get_text("classroom_name"),
            hint_text=self.get_text("enter_classroom_name"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
        )

        self.edit_classroom_level_field = TextField(
            label=self.get_text("level"),
            hint_text=self.get_text("enter_level"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
        )

        self.edit_classroom_dialog = AlertDialog(
            modal=True,
            scrollable=True,
            bgcolor="#f8faff",
            title=Container(
                content=Text(
                    self.get_text("edit_classroom"),
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
                                self.edit_classroom_name_field,
                                self.edit_classroom_level_field,
                            ],
                            spacing=10,
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                        ),
                    ],
                    spacing=15,
                    tight=True,
                ),
                width=500,
                padding=Padding.all(20),
                align=Alignment.CENTER_LEFT,
                alignment=Alignment.CENTER_LEFT,
                clip_behavior=ClipBehavior.HARD_EDGE,
                **self.get_box_style(),
            ),
            actions=[
                Button(
                    content=Text(self.get_text("cancel")),
                    on_click=self._close_classroom_edit_dialog,
                    style=ButtonStyle(
                        shape=RoundedRectangleBorder(radius=5),
                        bgcolor=Constants.CANCEL_COLOR,
                        padding=Padding(10, 20, 10, 20),
                        color="white",
                    ),
                ),
                Button(
                    content=Text(self.get_text("update")),
                    on_click=self._save_classroom_changes,
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

    def _build_school_year_edit_dialog(self):
        """Build school year edit dialog"""
        self.edit_school_year_name_field = TextField(
            label=self.get_text("school_year_name"),
            hint_text=self.get_text("enter_school_year_name"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
        )

        self.edit_school_year_start_date_field = TextField(
            label=self.get_text("start_date"),
            hint_text=self.get_text("enter_start_date"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            keyboard_type=KeyboardType.DATETIME,
        )

        self.edit_school_year_end_date_field = TextField(
            label=self.get_text("end_date"),
            hint_text=self.get_text("enter_end_date"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            keyboard_type=KeyboardType.DATETIME,
        )

        self.edit_school_year_status_switch = Switch(
            label=self.get_text("active"),
            value=False,
        )

        self.edit_school_year_dialog = AlertDialog(
            modal=True,
            scrollable=True,
            bgcolor="#f8faff",
            title=Container(
                content=Text(
                    self.get_text("edit_school_year"),
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
                                self.edit_school_year_name_field,
                            ],
                            spacing=10,
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        Row(
                            controls=[
                                self.edit_school_year_start_date_field,
                                self.edit_school_year_end_date_field,
                            ],
                            spacing=10,
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        Container(
                            content=self.edit_school_year_status_switch,
                            padding=Padding.symmetric(vertical=10),
                        ),
                    ],
                    spacing=15,
                    tight=True,
                ),
                width=550,
                padding=Padding.all(20),
                align=Alignment.CENTER_LEFT,
                alignment=Alignment.CENTER_LEFT,
                clip_behavior=ClipBehavior.HARD_EDGE,
                **self.get_box_style(),
            ),
            actions=[
                Button(
                    content=Text(self.get_text("cancel")),
                    on_click=self._close_school_year_edit_dialog,
                    style=ButtonStyle(
                        shape=RoundedRectangleBorder(radius=5),
                        bgcolor=Constants.CANCEL_COLOR,
                        padding=Padding(10, 20, 10, 20),
                        color="white",
                    ),
                ),
                Button(
                    content=Text(self.get_text("update")),
                    on_click=self._save_school_year_changes,
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

    def _build_staff_edit_dialog(self):
        """Build staff edit dialog"""
        self.edit_staff_first_name_field = TextField(
            label=self.get_text("first_name"),
            hint_text=self.get_text("enter_first_name"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
        )

        self.edit_staff_last_name_field = TextField(
            label=self.get_text("last_name"),
            hint_text=self.get_text("enter_last_name"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
        )

        self.edit_staff_position_field = TextField(
            label=self.get_text("position"),
            hint_text=self.get_text("enter_position"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
        )

        self.edit_staff_hire_date_field = TextField(
            label=self.get_text("hire_date"),
            hint_text=self.get_text("enter_hire_date"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            keyboard_type=KeyboardType.DATETIME,
        )

        self.edit_staff_salary_field = TextField(
            label=self.get_text("salary_base"),
            hint_text=self.get_text("enter_salary"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            keyboard_type=KeyboardType.NUMBER,
            input_filter=NumbersOnlyInputFilter(),
        )

        self.edit_staff_dialog = AlertDialog(
            modal=True,
            scrollable=True,
            bgcolor="#f8faff",
            title=Container(
                content=Text(
                    self.get_text("edit_staff"),
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
                                self.edit_staff_first_name_field,
                                self.edit_staff_last_name_field,
                            ],
                            spacing=10,
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        Row(
                            controls=[
                                self.edit_staff_position_field,
                                self.edit_staff_hire_date_field,
                            ],
                            spacing=10,
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        Row(
                            controls=[
                                self.edit_staff_salary_field,
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
                    on_click=self._close_staff_edit_dialog,
                    style=ButtonStyle(
                        shape=RoundedRectangleBorder(radius=5),
                        bgcolor=Constants.CANCEL_COLOR,
                        padding=Padding(10, 20, 10, 20),
                        color="white",
                    ),
                ),
                Button(
                    content=Text(self.get_text("update")),
                    on_click=self._save_staff_changes,
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

    # Dialog open methods
    def _open_user_edit_dialog(self, user: UserModel):
        """Open user edit dialog and populate with user data"""
        if not user:
            return

        # Store current editing user ID
        self.current_editing_user_id = user.id_user

        # Populate fields
        self.edit_user_username_field.value = user.username
        self.edit_user_email_field.value = user.email
        self.edit_user_password_field.value = user.password

        # Populate role dropdown
        self._populate_roles_dropdown_for_edit()
        self.edit_user_role_dropdown.value = str(user.role_id)

        # Open dialog
        self.page.show_dialog(self.edit_user_dialog)
        self.page.update()

    def _open_classroom_edit_dialog(self, classroom: ClassroomModel):
        """Open classroom edit dialog and populate with classroom data"""
        if not classroom:
            return

        # Store current editing classroom ID
        self.current_editing_classroom_id = classroom.id_classroom

        # Populate fields
        self.edit_classroom_name_field.value = classroom.name
        self.edit_classroom_level_field.value = classroom.level

        # Open dialog
        self.page.show_dialog(self.edit_classroom_dialog)
        self.page.update()

    def _open_school_year_edit_dialog(self, school_year: SchoolYearModel):
        """Open school year edit dialog and populate with school year data"""
        if not school_year:
            return

        # Store current editing school year ID
        self.current_editing_school_year_id = school_year.id_school_year

        # Populate fields
        self.edit_school_year_name_field.value = school_year.name
        self.edit_school_year_start_date_field.value = school_year.start_date
        self.edit_school_year_end_date_field.value = school_year.end_date
        self.edit_school_year_status_switch.value = school_year.is_active

        # Open dialog
        self.page.show_dialog(self.edit_school_year_dialog)
        self.page.update()

    def _open_staff_edit_dialog(self, staff: StaffModel):
        """Open staff edit dialog and populate with staff data"""
        if not staff:
            return

        # Store current editing staff ID
        self.current_editing_staff_id = staff.id_staff

        # Populate fields
        self.edit_staff_first_name_field.value = staff.first_name
        self.edit_staff_last_name_field.value = staff.last_name
        self.edit_staff_position_field.value = staff.position
        self.edit_staff_hire_date_field.value = staff.hire_date
        self.edit_staff_salary_field.value = str(int(staff.salary_base))

        # Open dialog
        self.page.show_dialog(self.edit_staff_dialog)
        self.page.update()

    # Dialog close methods
    def _close_user_edit_dialog(self, e=None):
        """Close user edit dialog"""
        self.edit_user_dialog.open = False
        self.page.update()

    def _close_classroom_edit_dialog(self, e=None):
        """Close classroom edit dialog"""
        self.edit_classroom_dialog.open = False
        self.page.update()

    def _close_school_year_edit_dialog(self, e=None):
        """Close school year edit dialog"""
        self.edit_school_year_dialog.open = False
        self.page.update()

    def _close_staff_edit_dialog(self, e=None):
        """Close staff edit dialog"""
        self.edit_staff_dialog.open = False
        self.page.update()

    # Save changes methods
    async def _save_user_changes(self, e):
        """Save changes to user"""
        # Validate fields
        if not self.edit_user_username_field.value:
            return

        if not self.edit_user_email_field.value:
            return

        # Update user data locally
        for i, user in enumerate(self.users_data):
            if user.id_user == self.current_editing_user_id:
                self.users_data[i].username = (
                    self.edit_user_username_field.value.strip()
                )
                self.users_data[i].email = self.edit_user_email_field.value.strip()
                self.users_data[i].password = (
                    self.edit_user_password_field.value.strip()
                )
                self.users_data[i].role_id = int(self.edit_user_role_dropdown.value)
                break

        # TODO: Call API to update user
        # success = await self.services.update_user(updated_user)

        # Close dialog
        self._close_user_edit_dialog()

        # Refresh table
        await self._update_user_table()

    async def _save_classroom_changes(self, e):
        """Save changes to classroom"""
        # Validate fields
        if not self.edit_classroom_name_field.value:
            return

        # Update classroom data locally
        for i, classroom in enumerate(self.classrooms_data):
            if classroom.id_classroom == self.current_editing_classroom_id:
                self.classrooms_data[i].name = (
                    self.edit_classroom_name_field.value.strip()
                )
                self.classrooms_data[i].level = (
                    self.edit_classroom_level_field.value.strip()
                )
                break

        # TODO: Call API to update classroom
        # success = await self.services.update_classroom(updated_classroom)

        # Close dialog
        self._close_classroom_edit_dialog()

        # Refresh table
        await self._update_classroom_table()

    async def _save_school_year_changes(self, e):
        """Save changes to school year"""
        # Validate fields
        if not self.edit_school_year_name_field.value:
            return

        # Update school year data locally
        for i, school_year in enumerate(self.school_year_data):
            if school_year.id_school_year == self.current_editing_school_year_id:
                self.school_year_data[i].name = (
                    self.edit_school_year_name_field.value.strip()
                )
                self.school_year_data[i].start_date = (
                    self.edit_school_year_start_date_field.value.strip()
                )
                self.school_year_data[i].end_date = (
                    self.edit_school_year_end_date_field.value.strip()
                )
                self.school_year_data[i].is_active = (
                    self.edit_school_year_status_switch.value
                )
                break

        # TODO: Call API to update school year
        # success = await self.services.update_school_year(updated_school_year)

        # Close dialog
        self._close_school_year_edit_dialog()

        # Refresh table
        await self._update_school_year_table()

    async def _save_staff_changes(self, e):
        """Save changes to staff"""
        # Validate fields
        if not self.edit_staff_first_name_field.value:
            return

        if not self.edit_staff_salary_field.value:
            return

        # Update staff data locally
        for i, staff in enumerate(self.staff_data):
            if staff.id_staff == self.current_editing_staff_id:
                self.staff_data[i].first_name = (
                    self.edit_staff_first_name_field.value.strip()
                )
                self.staff_data[i].last_name = (
                    self.edit_staff_last_name_field.value.strip()
                )
                self.staff_data[i].position = (
                    self.edit_staff_position_field.value.strip()
                )
                self.staff_data[i].hire_date = (
                    self.edit_staff_hire_date_field.value.strip()
                )
                self.staff_data[i].salary_base = float(
                    self.edit_staff_salary_field.value
                )
                break

        # TODO: Call API to update staff
        # success = await self.services.update_staff(updated_staff)

        # Close dialog
        self._close_staff_edit_dialog()

        # Refresh table
        await self._update_staff_table()

    def _populate_roles_dropdown_for_edit(self):
        """Populate roles dropdown for edit dialog"""
        self.edit_user_role_dropdown.options = [
            DropdownOption(key="1", text="Administrateur"),
            DropdownOption(key="2", text="Enseignant"),
            DropdownOption(key="3", text="Comptable"),
            DropdownOption(key="4", text="Surveillant"),
        ]

    #################################################################
    # ----------------------  DELETE DIALOGS -----------------------#

    def _build_delete_dialogs(self):
        """Build all delete dialogs"""
        self._build_user_delete_dialog()
        self._build_classroom_delete_dialog()
        self._build_school_year_delete_dialog()
        self._build_staff_delete_dialog()

    def _build_user_delete_dialog(self):
        """Build user delete dialog"""
        self.delete_user_motive_field = TextField(
            label=self.get_text("motive"),
            hint_text=self.get_text("enter_motive"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=True,
            multiline=True,
            min_lines=2,
            max_lines=5,
        )

        self.user_name_to_be_deleted = Text(
            value="",
            weight=FontWeight.BOLD,
            size=16,
        )

        self.delete_user_dialog = AlertDialog(
            modal=True,
            scrollable=True,
            bgcolor="#f8faff",
            title=Container(
                content=Text(
                    self.get_text("delete_user"),
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
                            self.get_text("confirm_delete_user"),
                            size=14,
                            color=Constants.PRIMARY_COLOR,
                        ),
                        self.user_name_to_be_deleted,
                        self.delete_user_motive_field,
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
                **self.get_box_style(),
            ),
            actions=[
                Button(
                    content=Text(self.get_text("cancel")),
                    on_click=self._close_user_delete_dialog,
                    style=ButtonStyle(
                        shape=RoundedRectangleBorder(radius=5),
                        bgcolor=Constants.PRIMARY_COLOR,
                        padding=Padding(10, 20, 10, 20),
                        color="white",
                    ),
                ),
                Button(
                    content=Text(self.get_text("delete")),
                    on_click=self._confirm_delete_user,
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

    def _build_classroom_delete_dialog(self):
        """Build classroom delete dialog"""
        self.delete_classroom_motive_field = TextField(
            label=self.get_text("motive"),
            hint_text=self.get_text("enter_motive"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=True,
            multiline=True,
            min_lines=2,
            max_lines=5,
        )

        self.classroom_name_to_be_deleted = Text(
            value="",
            weight=FontWeight.BOLD,
            size=16,
        )

        self.delete_classroom_dialog = AlertDialog(
            modal=True,
            scrollable=True,
            bgcolor="#f8faff",
            title=Container(
                content=Text(
                    self.get_text("delete_classroom"),
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
                            self.get_text("confirm_delete_classroom"),
                            size=14,
                            color=Constants.PRIMARY_COLOR,
                        ),
                        self.classroom_name_to_be_deleted,
                        self.delete_classroom_motive_field,
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
                **self.get_box_style(),
            ),
            actions=[
                Button(
                    content=Text(self.get_text("cancel")),
                    on_click=self._close_classroom_delete_dialog,
                    style=ButtonStyle(
                        shape=RoundedRectangleBorder(radius=5),
                        bgcolor=Constants.PRIMARY_COLOR,
                        padding=Padding(10, 20, 10, 20),
                        color="white",
                    ),
                ),
                Button(
                    content=Text(self.get_text("delete")),
                    on_click=self._confirm_delete_classroom,
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

    def _build_school_year_delete_dialog(self):
        """Build school year delete dialog"""
        self.delete_school_year_motive_field = TextField(
            label=self.get_text("motive"),
            hint_text=self.get_text("enter_motive"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=True,
            multiline=True,
            min_lines=2,
            max_lines=5,
        )

        self.school_year_name_to_be_deleted = Text(
            value="",
            weight=FontWeight.BOLD,
            size=16,
        )

        self.delete_school_year_dialog = AlertDialog(
            modal=True,
            scrollable=True,
            bgcolor="#f8faff",
            title=Container(
                content=Text(
                    self.get_text("delete_school_year"),
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
                            self.get_text("confirm_delete_school_year"),
                            size=14,
                            color=Constants.PRIMARY_COLOR,
                        ),
                        self.school_year_name_to_be_deleted,
                        self.delete_school_year_motive_field,
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
                **self.get_box_style(),
            ),
            actions=[
                Button(
                    content=Text(self.get_text("cancel")),
                    on_click=self._close_school_year_delete_dialog,
                    style=ButtonStyle(
                        shape=RoundedRectangleBorder(radius=5),
                        bgcolor=Constants.PRIMARY_COLOR,
                        padding=Padding(10, 20, 10, 20),
                        color="white",
                    ),
                ),
                Button(
                    content=Text(self.get_text("delete")),
                    on_click=self._confirm_delete_school_year,
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

    def _build_staff_delete_dialog(self):
        """Build staff delete dialog"""
        self.delete_staff_motive_field = TextField(
            label=self.get_text("motive"),
            hint_text=self.get_text("enter_motive"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=True,
            multiline=True,
            min_lines=2,
            max_lines=5,
        )

        self.staff_name_to_be_deleted = Text(
            value="",
            weight=FontWeight.BOLD,
            size=16,
        )

        self.delete_staff_dialog = AlertDialog(
            modal=True,
            scrollable=True,
            bgcolor="#f8faff",
            title=Container(
                content=Text(
                    self.get_text("delete_staff"),
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
                            self.get_text("confirm_delete_staff"),
                            size=14,
                            color=Constants.PRIMARY_COLOR,
                        ),
                        self.staff_name_to_be_deleted,
                        self.delete_staff_motive_field,
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
                **self.get_box_style(),
            ),
            actions=[
                Button(
                    content=Text(self.get_text("cancel")),
                    on_click=self._close_staff_delete_dialog,
                    style=ButtonStyle(
                        shape=RoundedRectangleBorder(radius=5),
                        bgcolor=Constants.PRIMARY_COLOR,
                        padding=Padding(10, 20, 10, 20),
                        color="white",
                    ),
                ),
                Button(
                    content=Text(self.get_text("delete")),
                    on_click=self._confirm_delete_staff,
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

    # Dialog open methods for delete
    def _open_user_delete_dialog(self, user: UserModel):
        """Open user delete dialog"""
        if not user:
            return

        # Store current deleting user ID
        self.current_deleting_user_id = user.id_user

        # Set user name
        self.user_name_to_be_deleted.value = user.username

        # Clear motive field
        self.delete_user_motive_field.value = ""

        # Open dialog
        self.page.show_dialog(self.delete_user_dialog)
        self.page.update()

    def _open_classroom_delete_dialog(self, classroom: ClassroomModel):
        """Open classroom delete dialog"""
        if not classroom:
            return

        # Store current deleting classroom ID
        self.current_deleting_classroom_id = classroom.id_classroom

        # Set classroom name
        self.classroom_name_to_be_deleted.value = classroom.name

        # Clear motive field
        self.delete_classroom_motive_field.value = ""

        # Open dialog
        self.page.show_dialog(self.delete_classroom_dialog)
        self.page.update()

    def _open_school_year_delete_dialog(self, school_year: SchoolYearModel):
        """Open school year delete dialog"""
        if not school_year:
            return

        # Store current deleting school year ID
        self.current_deleting_school_year_id = school_year.id_school_year

        # Set school year name
        self.school_year_name_to_be_deleted.value = school_year.name

        # Clear motive field
        self.delete_school_year_motive_field.value = ""

        # Open dialog
        self.page.show_dialog(self.delete_school_year_dialog)
        self.page.update()

    def _open_staff_delete_dialog(self, staff: StaffModel):
        """Open staff delete dialog"""
        if not staff:
            return

        # Store current deleting staff ID
        self.current_deleting_staff_id = staff.id_staff

        # Set staff name
        full_name = f"{staff.first_name} {staff.last_name}"
        self.staff_name_to_be_deleted.value = full_name

        # Clear motive field
        self.delete_staff_motive_field.value = ""

        # Open dialog
        self.page.show_dialog(self.delete_staff_dialog)
        self.page.update()

    # Dialog close methods for delete
    def _close_user_delete_dialog(self, e=None):
        """Close user delete dialog"""
        self.delete_user_dialog.open = False
        self.page.update()

    def _close_classroom_delete_dialog(self, e=None):
        """Close classroom delete dialog"""
        self.delete_classroom_dialog.open = False
        self.page.update()

    def _close_school_year_delete_dialog(self, e=None):
        """Close school year delete dialog"""
        self.delete_school_year_dialog.open = False
        self.page.update()

    def _close_staff_delete_dialog(self, e=None):
        """Close staff delete dialog"""
        self.delete_staff_dialog.open = False
        self.page.update()

    # Confirm delete methods
    async def _confirm_delete_user(self, e):
        """Confirm deletion of user"""
        # Validate motive
        if (
            not self.delete_user_motive_field.value
            or not self.delete_user_motive_field.value.strip()
        ):
            return

        # Remove user from local data
        self.users_data = [
            u for u in self.users_data if u.id_user != self.current_deleting_user_id
        ]

        # TODO: Call API to delete user
        # success = await self.services.delete_user(self.current_deleting_user_id, self.delete_user_motive_field.value)

        # Close dialog
        self._close_user_delete_dialog()

        # Refresh table
        await self._update_user_table()

    async def _confirm_delete_classroom(self, e):
        """Confirm deletion of classroom"""
        # Validate motive
        if (
            not self.delete_classroom_motive_field.value
            or not self.delete_classroom_motive_field.value.strip()
        ):
            return

        # Remove classroom from local data
        self.classrooms_data = [
            c
            for c in self.classrooms_data
            if c.id_classroom != self.current_deleting_classroom_id
        ]

        # TODO: Call API to delete classroom
        # success = await self.services.delete_classroom(self.current_deleting_classroom_id, self.delete_classroom_motive_field.value)

        # Close dialog
        self._close_classroom_delete_dialog()

        # Refresh table
        await self._update_classroom_table()

    async def _confirm_delete_school_year(self, e):
        """Confirm deletion of school year"""
        # Validate motive
        if (
            not self.delete_school_year_motive_field.value
            or not self.delete_school_year_motive_field.value.strip()
        ):
            return

        # Remove school year from local data
        self.school_year_data = [
            sy
            for sy in self.school_year_data
            if sy.id_school_year != self.current_deleting_school_year_id
        ]

        # TODO: Call API to delete school year
        # success = await self.services.delete_school_year(self.current_deleting_school_year_id, self.delete_school_year_motive_field.value)

        # Close dialog
        self._close_school_year_delete_dialog()

        # Refresh table
        await self._update_school_year_table()

    async def _confirm_delete_staff(self, e):
        """Confirm deletion of staff"""
        # Validate motive
        if (
            not self.delete_staff_motive_field.value
            or not self.delete_staff_motive_field.value.strip()
        ):
            return

        # Remove staff from local data
        self.staff_data = [
            s for s in self.staff_data if s.id_staff != self.current_deleting_staff_id
        ]

        # TODO: Call API to delete staff
        # success = await self.services.delete_staff(self.current_deleting_staff_id, self.delete_staff_motive_field.value)

        # Close dialog
        self._close_staff_delete_dialog()

        # Refresh table
        await self._update_staff_table()

    #################################################################
    # ----------------------  TABLES -------------------------------#

    # ------------- USERS TABLE
    def _create_users_table_header(self):
        """Create table header row"""
        return Container(
            content=Row(
                controls=[
                    Container(
                        content=Text(
                            self.get_text("username"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.get_text("email"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=3,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.get_text("password"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.get_text("role"),
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
            height=65,
        )

    async def _create_user_table_row(self, user: UserModel, index):
        """Create a table row for a user"""
        user_name = user.username
        user_email = user.email
        user_password = user.password
        user_role = await self.services.get_user_role_by_user_id(user.id_user)

        row_color = "#f8faff" if index % 2 == 0 else "#ffffff"

        return Container(
            content=Row(
                controls=[
                    Container(
                        content=Text(user_name, size=14),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(user_email, size=14),
                        expand=3,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(user_password, size=14),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            Utils.trunc_text(user_role, length=5),
                            size=14,
                            color=Colors.WHITE,
                        ),
                        expand=1,
                        padding=Padding.all(10),
                        bgcolor=self.get_color_by_user_role(user_role),
                        border_radius=BorderRadius.all(10),
                    ),
                    Container(
                        content=Row(
                            controls=[
                                IconButton(
                                    icon=Icons.EDIT,
                                    icon_color=Constants.PRIMARY_COLOR,
                                    tooltip=self.get_text("edit"),
                                    on_click=lambda e, u=user: self._open_user_edit_dialog(
                                        u
                                    ),
                                ),
                                IconButton(
                                    icon=Icons.DELETE,
                                    icon_color=Constants.CANCEL_COLOR,
                                    tooltip=self.get_text("delete"),
                                    on_click=lambda e, u=user: self._open_user_delete_dialog(
                                        u
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

    async def _update_user_table(self):
        """Update the users table with current data"""

        # Build table content
        table_controls = [self._create_users_table_header()]

        # Update add button
        self.add_action_button.content = self.get_text("new_user")

        if not self.users_data:
            # No students found message
            table_controls.append(
                Container(
                    content=Column(
                        controls=[
                            Icon(Icons.SEARCH_OFF, size=60, color=Colors.GREY_400),
                            Text(
                                self.get_text("no_users_found"),
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
            # Add user rows
            for index, user in enumerate(self.users_data):
                table_controls.append(await self._create_user_table_row(user, index))

        self.data_table_container.content = Column(
            controls=table_controls,
            scroll=ScrollMode.AUTO,
            spacing=0,
        )

        try:
            self.add_action_button.update()
            self.data_table_container.update()
        except Exception as e:
            # print("Error updating table:", e)
            pass

    # ------------- CLASSROOMS TABLE
    def _create_classrooms_table_header(self):
        """Create classrooms table header row"""
        return Container(
            content=Row(
                controls=[
                    Container(
                        content=Text(
                            self.get_text("classroom"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=3,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.get_text("level"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=3,
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
            height=65,
        )

    def _create_classroom_table_row(self, classroom: ClassroomModel, index):
        """Create a table row for a classroom"""
        classroom_name = classroom.name
        classroom_level = classroom.level

        row_color = "#f8faff" if index % 2 == 0 else "#ffffff"

        return Container(
            content=Row(
                controls=[
                    Container(
                        content=Text(classroom_name, size=14),
                        expand=3,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(classroom_level, size=14),
                        expand=3,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Row(
                            controls=[
                                IconButton(
                                    icon=Icons.EDIT,
                                    icon_color=Constants.PRIMARY_COLOR,
                                    tooltip=self.get_text("edit"),
                                    on_click=lambda e, c=classroom: self._open_classroom_edit_dialog(
                                        c
                                    ),
                                ),
                                IconButton(
                                    icon=Icons.DELETE,
                                    icon_color=Constants.CANCEL_COLOR,
                                    tooltip=self.get_text("delete"),
                                    on_click=lambda e, c=classroom: self._open_classroom_delete_dialog(
                                        c
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

    async def _update_classroom_table(self):
        """Update the classrooms table with current data"""

        # Build table content
        table_controls = [self._create_classrooms_table_header()]

        # Update add button
        self.add_action_button.content = self.get_text("new_classroom")

        if not self.classrooms_data:
            # No students found message
            table_controls.append(
                Container(
                    content=Column(
                        controls=[
                            Icon(Icons.SEARCH_OFF, size=60, color=Colors.GREY_400),
                            Text(
                                self.get_text("no_classrooms_found"),
                                size=18,
                                weight=FontWeight.BOLD,
                                color=Colors.GREY_600,
                            ),
                            Text(
                                self.get_text("no_classrooms_message"),
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
            # Add classrooms rows
            for index, classroom in enumerate(self.classrooms_data):
                table_controls.append(
                    self._create_classroom_table_row(classroom, index)
                )

        self.data_table_container.content = Column(
            controls=table_controls,
            scroll=ScrollMode.AUTO,
            spacing=0,
        )

        try:
            self.add_action_button.update()
            self.data_table_container.update()
        except Exception as e:
            # print("Error updating table:", e)
            pass

    # ------------- SCHOOL YEARS TABLE
    def _create_school_years_table_header(self):
        """Create school years table header row"""
        return Container(
            content=Row(
                controls=[
                    Container(
                        content=Text(
                            self.get_text("name"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.get_text("start_date"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.get_text("end_date"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.get_text("is_active"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=2,
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
            height=65,
        )

    def _create_school_year_table_row(self, school_year: SchoolYearModel, index):
        """Create a table row for a school year"""
        school_year_name = school_year.name
        start_date = school_year.start_date
        end_date = school_year.end_date
        is_active = school_year.is_active

        row_color = "#f8faff" if index % 2 == 0 else "#ffffff"

        return Container(
            content=Row(
                controls=[
                    Container(
                        content=Text(school_year_name, size=14),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(start_date, size=14),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(end_date, size=14),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Switch(
                            value=is_active,
                            disabled=is_active,
                            active_color=Constants.PRIMARY_COLOR,
                            data=school_year,
                            overlay_color={
                                ControlState.DISABLED: Constants.PRIMARY_COLOR,
                            },
                        ),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Row(
                            controls=[
                                IconButton(
                                    icon=Icons.EDIT,
                                    icon_color=Constants.PRIMARY_COLOR,
                                    tooltip=self.get_text("edit"),
                                    on_click=lambda e, sy=school_year: self._open_school_year_edit_dialog(
                                        sy
                                    ),
                                ),
                                IconButton(
                                    icon=Icons.DELETE,
                                    icon_color=Constants.CANCEL_COLOR,
                                    tooltip=self.get_text("delete"),
                                    on_click=lambda e, sy=school_year: self._open_school_year_delete_dialog(
                                        sy
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

    async def _update_school_year_table(self):
        """Update the school year table with current data"""

        # Build table content
        table_controls = [self._create_school_years_table_header()]

        # Update add button
        self.add_action_button.content = self.get_text("new_school_year")

        if not self.school_year_data:
            # No students found message
            table_controls.append(
                Container(
                    content=Column(
                        controls=[
                            Icon(Icons.SEARCH_OFF, size=60, color=Colors.GREY_400),
                            Text(
                                self.get_text("no_school_years_found"),
                                size=18,
                                weight=FontWeight.BOLD,
                                color=Colors.GREY_600,
                            ),
                            Text(
                                self.get_text("no_school_years_message"),
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
            # Add classrooms rows
            for index, school_year in enumerate(self.school_year_data):
                table_controls.append(
                    self._create_school_year_table_row(school_year, index)
                )

        self.data_table_container.content = Column(
            controls=table_controls,
            scroll=ScrollMode.AUTO,
            spacing=0,
        )

        try:
            self.add_action_button.update()
            self.data_table_container.update()
        except Exception as e:
            # print("Error updating table:", e)
            pass

    # ------------- STAFF TABLE
    def _create_staff_table_header(self):
        """Create staff table header row"""
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
                            self.get_text("position"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.get_text("hire_date"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.get_text("salary_base"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=2,
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
            height=65,
        )

    def _create_staff_table_row(self, staff: StaffModel, index):
        """Create a table row for a staff"""
        full_name = f"{staff.first_name} {staff.last_name}"
        position = staff.position
        hire_date = staff.hire_date
        salary_base = f"{staff.salary_base:.1f} Fc" if staff.salary_base else "0.0 Fc"

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
                        content=Text(position, size=14),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(hire_date, size=14),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(salary_base, size=14),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Row(
                            controls=[
                                IconButton(
                                    icon=Icons.EDIT,
                                    icon_color=Constants.PRIMARY_COLOR,
                                    tooltip=self.get_text("edit"),
                                    on_click=lambda e, s=staff: self._open_staff_edit_dialog(
                                        s
                                    ),
                                ),
                                IconButton(
                                    icon=Icons.DELETE,
                                    icon_color=Constants.CANCEL_COLOR,
                                    tooltip=self.get_text("delete"),
                                    on_click=lambda e, s=staff: self._open_staff_delete_dialog(
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
        )

    async def _update_staff_table(self):
        """Update the staff table with current data"""

        # Build table content
        table_controls = [self._create_staff_table_header()]

        # Update add button
        self.add_action_button.content = self.get_text("new_staff")

        if not self.staff_data:
            # No students found message
            table_controls.append(
                Container(
                    content=Column(
                        controls=[
                            Icon(Icons.SEARCH_OFF, size=60, color=Colors.GREY_400),
                            Text(
                                self.get_text("no_staff_found"),
                                size=18,
                                weight=FontWeight.BOLD,
                                color=Colors.GREY_600,
                            ),
                            Text(
                                self.get_text("no_staff_message"),
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
            # Add classrooms rows
            for index, staff in enumerate(self.staff_data):
                table_controls.append(self._create_staff_table_row(staff, index))

        self.data_table_container.content = Column(
            controls=table_controls,
            scroll=ScrollMode.AUTO,
            spacing=0,
        )

        try:
            self.add_action_button.update()
            self.data_table_container.update()
        except Exception as e:
            # print("Error updating table:", e)
            pass

    def create_stat_card(
        self, title: str, value: str, icon: str, color: str, subtitle: str = None
    ) -> Control:
        """Create a statistics card"""
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

    def build(self) -> Column:
        return Column(
            horizontal_alignment=CrossAxisAlignment.STRETCH,
            controls=[
                Container(
                    content=Row(
                        controls=[
                            Text(
                                value=self.get_text("admin"),
                                size=24,
                                weight=FontWeight.BOLD,
                                color=Constants.PRIMARY_COLOR,
                            ),
                            IconButton(
                                icon=Icons.REFRESH,
                                icon_color=Constants.PRIMARY_COLOR,
                                tooltip=self.get_text("refresh"),
                                on_click=self.refresh_admin_data,
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

    ######################################################################
    #####################     SERVICES CALLBACK   ########################

    async def _activate_school_year(self, e: Event):
        pass
