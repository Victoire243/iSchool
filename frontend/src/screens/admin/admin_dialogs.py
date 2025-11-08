"""
Module de gestion des dialogues d'édition et de suppression pour l'écran Admin
"""

import flet as ft
from flet import (
    AlertDialog,
    Button,
    ButtonStyle,
    Container,
    Column,
    Row,
    Text,
    TextField,
    Dropdown,
    DropdownOption,
    Switch,
    Padding,
    BorderRadius,
    MainAxisAlignment,
    CrossAxisAlignment,
    Alignment,
    FontWeight,
    ClipBehavior,
    RoundedRectangleBorder,
    KeyboardType,
)
from core.constants import Constants
from models.user_model import UserModel
from models.classroom_model import ClassroomModel
from models.school_year_model import SchoolYearModel
from models.staff_model import StaffModel


class AdminDialogs:
    """Gestionnaire des dialogues d'édition et de suppression"""

    def __init__(self, parent):
        """
        Initialize AdminDialogs

        Args:
            parent: Instance de AdminScreen qui contient ce module
        """
        self.parent = parent

        # IDs des éléments en cours d'édition/suppression
        self.current_editing_user_id = None
        self.current_editing_classroom_id = None
        self.current_editing_school_year_id = None
        self.current_editing_staff_id = None

        self.current_deleting_user_id = None
        self.current_deleting_classroom_id = None
        self.current_deleting_school_year_id = None
        self.current_deleting_staff_id = None

    def build_all_dialogs(self):
        """Construire tous les dialogues"""
        self._build_edit_dialogs()
        self._build_delete_dialogs()

    #################################################################
    # DIALOGUES D'ÉDITION
    #################################################################

    def _build_edit_dialogs(self):
        """Construire tous les dialogues d'édition"""
        self._build_user_edit_dialog()
        self._build_classroom_edit_dialog()
        self._build_school_year_edit_dialog()
        self._build_staff_edit_dialog()

    def _build_user_edit_dialog(self):
        """Construire le dialogue d'édition utilisateur"""
        self.edit_user_username_field = TextField(
            label=self.parent.get_text("username"),
            hint_text=self.parent.get_text("enter_username"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
        )

        self.edit_user_email_field = TextField(
            label=self.parent.get_text("email"),
            hint_text=self.parent.get_text("enter_email"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            keyboard_type=KeyboardType.EMAIL,
        )

        self.edit_user_password_field = TextField(
            label=self.parent.get_text("password"),
            hint_text=self.parent.get_text("enter_password"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            password=True,
            can_reveal_password=True,
        )

        self.edit_user_role_dropdown = Dropdown(
            label=self.parent.get_text("role"),
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
                    self.parent.get_text("edit_user"),
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
                **self.parent.get_box_style(),
            ),
            actions=[
                Button(
                    content=Text(self.parent.get_text("cancel")),
                    on_click=self._close_user_edit_dialog,
                    style=ButtonStyle(
                        shape=RoundedRectangleBorder(radius=5),
                        bgcolor=Constants.CANCEL_COLOR,
                        padding=Padding(10, 20, 10, 20),
                        color="white",
                    ),
                ),
                Button(
                    content=Text(self.parent.get_text("update")),
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
        """Construire le dialogue d'édition classe"""
        self.edit_classroom_name_field = TextField(
            label=self.parent.get_text("classroom_name"),
            hint_text=self.parent.get_text("enter_classroom_name"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
        )

        self.edit_classroom_level_field = TextField(
            label=self.parent.get_text("level"),
            hint_text=self.parent.get_text("enter_level"),
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
                    self.parent.get_text("edit_classroom"),
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
                **self.parent.get_box_style(),
            ),
            actions=[
                Button(
                    content=Text(self.parent.get_text("cancel")),
                    on_click=self._close_classroom_edit_dialog,
                    style=ButtonStyle(
                        shape=RoundedRectangleBorder(radius=5),
                        bgcolor=Constants.CANCEL_COLOR,
                        padding=Padding(10, 20, 10, 20),
                        color="white",
                    ),
                ),
                Button(
                    content=Text(self.parent.get_text("update")),
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
        """Construire le dialogue d'édition année scolaire"""
        self.edit_school_year_name_field = TextField(
            label=self.parent.get_text("school_year_name"),
            hint_text=self.parent.get_text("enter_school_year_name"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
        )

        self.edit_school_year_start_date_field = TextField(
            label=self.parent.get_text("start_date"),
            hint_text="YYYY-MM-DD",
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
        )

        self.edit_school_year_end_date_field = TextField(
            label=self.parent.get_text("end_date"),
            hint_text="YYYY-MM-DD",
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
        )

        self.edit_school_year_status_switch = Switch(
            label=self.parent.get_text("active"),
            value=False,
            active_color=Constants.PRIMARY_COLOR,
        )

        self.edit_school_year_dialog = AlertDialog(
            modal=True,
            scrollable=True,
            bgcolor="#f8faff",
            title=Container(
                content=Text(
                    self.parent.get_text("edit_school_year"),
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
                        self.edit_school_year_name_field,
                        Row(
                            controls=[
                                self.edit_school_year_start_date_field,
                                self.edit_school_year_end_date_field,
                            ],
                            spacing=10,
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        self.edit_school_year_status_switch,
                    ],
                    spacing=15,
                    tight=True,
                ),
                width=550,
                padding=Padding.all(20),
                align=Alignment.CENTER_LEFT,
                alignment=Alignment.CENTER_LEFT,
                clip_behavior=ClipBehavior.HARD_EDGE,
                **self.parent.get_box_style(),
            ),
            actions=[
                Button(
                    content=Text(self.parent.get_text("cancel")),
                    on_click=self._close_school_year_edit_dialog,
                    style=ButtonStyle(
                        shape=RoundedRectangleBorder(radius=5),
                        bgcolor=Constants.CANCEL_COLOR,
                        padding=Padding(10, 20, 10, 20),
                        color="white",
                    ),
                ),
                Button(
                    content=Text(self.parent.get_text("update")),
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
        """Construire le dialogue d'édition personnel"""
        self.edit_staff_first_name_field = TextField(
            label=self.parent.get_text("first_name"),
            hint_text=self.parent.get_text("enter_first_name"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
        )

        self.edit_staff_last_name_field = TextField(
            label=self.parent.get_text("last_name"),
            hint_text=self.parent.get_text("enter_last_name"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
        )

        self.edit_staff_position_field = TextField(
            label=self.parent.get_text("position"),
            hint_text=self.parent.get_text("enter_position"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
        )

        self.edit_staff_hire_date_field = TextField(
            label=self.parent.get_text("hire_date"),
            hint_text="YYYY-MM-DD",
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
        )

        self.edit_staff_salary_field = TextField(
            label=self.parent.get_text("salary"),
            hint_text=self.parent.get_text("enter_salary"),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            keyboard_type=KeyboardType.NUMBER,
        )

        self.edit_staff_dialog = AlertDialog(
            modal=True,
            scrollable=True,
            bgcolor="#f8faff",
            title=Container(
                content=Text(
                    self.parent.get_text("edit_staff"),
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
                        self.edit_staff_salary_field,
                    ],
                    spacing=15,
                    tight=True,
                ),
                width=600,
                padding=Padding.all(20),
                align=Alignment.CENTER_LEFT,
                alignment=Alignment.CENTER_LEFT,
                clip_behavior=ClipBehavior.HARD_EDGE,
                **self.parent.get_box_style(),
            ),
            actions=[
                Button(
                    content=Text(self.parent.get_text("cancel")),
                    on_click=self._close_staff_edit_dialog,
                    style=ButtonStyle(
                        shape=RoundedRectangleBorder(radius=5),
                        bgcolor=Constants.CANCEL_COLOR,
                        padding=Padding(10, 20, 10, 20),
                        color="white",
                    ),
                ),
                Button(
                    content=Text(self.parent.get_text("update")),
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

    #################################################################
    # DIALOGUES DE SUPPRESSION
    #################################################################

    def _build_delete_dialogs(self):
        """Construire tous les dialogues de suppression"""
        self._build_user_delete_dialog()
        self._build_classroom_delete_dialog()
        self._build_school_year_delete_dialog()
        self._build_staff_delete_dialog()

    def _build_user_delete_dialog(self):
        """Construire le dialogue de suppression utilisateur"""
        self.delete_user_motive_field = TextField(
            label=self.parent.get_text("motive"),
            hint_text=self.parent.get_text("enter_motive"),
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
                    self.parent.get_text("delete_user"),
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
                            self.parent.get_text("confirm_delete_user"),
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
                **self.parent.get_box_style(),
            ),
            actions=[
                Button(
                    content=Text(self.parent.get_text("cancel")),
                    on_click=self._close_user_delete_dialog,
                    style=ButtonStyle(
                        shape=RoundedRectangleBorder(radius=5),
                        bgcolor=Constants.PRIMARY_COLOR,
                        padding=Padding(10, 20, 10, 20),
                        color="white",
                    ),
                ),
                Button(
                    content=Text(self.parent.get_text("delete")),
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
        """Construire le dialogue de suppression classe"""
        self.delete_classroom_motive_field = TextField(
            label=self.parent.get_text("motive"),
            hint_text=self.parent.get_text("enter_motive"),
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
                    self.parent.get_text("delete_classroom"),
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
                            self.parent.get_text("confirm_delete_classroom"),
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
                **self.parent.get_box_style(),
            ),
            actions=[
                Button(
                    content=Text(self.parent.get_text("cancel")),
                    on_click=self._close_classroom_delete_dialog,
                    style=ButtonStyle(
                        shape=RoundedRectangleBorder(radius=5),
                        bgcolor=Constants.PRIMARY_COLOR,
                        padding=Padding(10, 20, 10, 20),
                        color="white",
                    ),
                ),
                Button(
                    content=Text(self.parent.get_text("delete")),
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
        """Construire le dialogue de suppression année scolaire"""
        self.delete_school_year_motive_field = TextField(
            label=self.parent.get_text("motive"),
            hint_text=self.parent.get_text("enter_motive"),
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
                    self.parent.get_text("delete_school_year"),
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
                            self.parent.get_text("confirm_delete_school_year"),
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
                **self.parent.get_box_style(),
            ),
            actions=[
                Button(
                    content=Text(self.parent.get_text("cancel")),
                    on_click=self._close_school_year_delete_dialog,
                    style=ButtonStyle(
                        shape=RoundedRectangleBorder(radius=5),
                        bgcolor=Constants.PRIMARY_COLOR,
                        padding=Padding(10, 20, 10, 20),
                        color="white",
                    ),
                ),
                Button(
                    content=Text(self.parent.get_text("delete")),
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
        """Construire le dialogue de suppression personnel"""
        self.delete_staff_motive_field = TextField(
            label=self.parent.get_text("motive"),
            hint_text=self.parent.get_text("enter_motive"),
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
                    self.parent.get_text("delete_staff"),
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
                            self.parent.get_text("confirm_delete_staff"),
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
                **self.parent.get_box_style(),
            ),
            actions=[
                Button(
                    content=Text(self.parent.get_text("cancel")),
                    on_click=self._close_staff_delete_dialog,
                    style=ButtonStyle(
                        shape=RoundedRectangleBorder(radius=5),
                        bgcolor=Constants.PRIMARY_COLOR,
                        padding=Padding(10, 20, 10, 20),
                        color="white",
                    ),
                ),
                Button(
                    content=Text(self.parent.get_text("delete")),
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

    #################################################################
    # MÉTHODES D'OUVERTURE DES DIALOGUES D'ÉDITION
    #################################################################

    def open_user_edit_dialog(self, user: UserModel):
        """Ouvrir le dialogue d'édition utilisateur"""
        if not user:
            return

        self.current_editing_user_id = user.id_user
        self.edit_user_username_field.value = user.username
        self.edit_user_email_field.value = user.email
        self.edit_user_password_field.value = user.password

        # Peupler le dropdown des rôles
        self._populate_roles_dropdown_for_edit()
        self.edit_user_role_dropdown.value = str(user.role_id)

        self.parent.page.show_dialog(self.edit_user_dialog)
        self.parent.page.update()

    def open_classroom_edit_dialog(self, classroom: ClassroomModel):
        """Ouvrir le dialogue d'édition classe"""
        if not classroom:
            return

        self.current_editing_classroom_id = classroom.id_classroom
        self.edit_classroom_name_field.value = classroom.name
        self.edit_classroom_level_field.value = classroom.level

        self.parent.page.show_dialog(self.edit_classroom_dialog)
        self.parent.page.update()

    def open_school_year_edit_dialog(self, school_year: SchoolYearModel):
        """Ouvrir le dialogue d'édition année scolaire"""
        if not school_year:
            return

        self.current_editing_school_year_id = school_year.id_school_year
        self.edit_school_year_name_field.value = school_year.name
        self.edit_school_year_start_date_field.value = school_year.start_date
        self.edit_school_year_end_date_field.value = school_year.end_date
        self.edit_school_year_status_switch.value = school_year.is_active

        self.parent.page.show_dialog(self.edit_school_year_dialog)
        self.parent.page.update()

    def open_staff_edit_dialog(self, staff: StaffModel):
        """Ouvrir le dialogue d'édition personnel"""
        if not staff:
            return

        self.current_editing_staff_id = staff.id_staff
        self.edit_staff_first_name_field.value = staff.first_name
        self.edit_staff_last_name_field.value = staff.last_name
        self.edit_staff_position_field.value = staff.position
        self.edit_staff_hire_date_field.value = staff.hire_date
        self.edit_staff_salary_field.value = str(int(staff.salary_base))

        self.parent.page.show_dialog(self.edit_staff_dialog)
        self.parent.page.update()

    #################################################################
    # MÉTHODES DE FERMETURE DES DIALOGUES D'ÉDITION
    #################################################################

    def _close_user_edit_dialog(self, e=None):
        """Fermer le dialogue d'édition utilisateur"""
        self.edit_user_dialog.open = False
        self.parent.page.update()

    def _close_classroom_edit_dialog(self, e=None):
        """Fermer le dialogue d'édition classe"""
        self.edit_classroom_dialog.open = False
        self.parent.page.update()

    def _close_school_year_edit_dialog(self, e=None):
        """Fermer le dialogue d'édition année scolaire"""
        self.edit_school_year_dialog.open = False
        self.parent.page.update()

    def _close_staff_edit_dialog(self, e=None):
        """Fermer le dialogue d'édition personnel"""
        self.edit_staff_dialog.open = False
        self.parent.page.update()

    #################################################################
    # MÉTHODES DE SAUVEGARDE DES MODIFICATIONS
    #################################################################

    async def _save_user_changes(self, e):
        """Sauvegarder les modifications utilisateur"""
        if not self.edit_user_username_field.value:
            return
        if not self.edit_user_email_field.value:
            return

        # Mettre à jour les données localement
        for i, user in enumerate(self.parent.users_data):
            if user.id_user == self.current_editing_user_id:
                self.parent.users_data[i].username = (
                    self.edit_user_username_field.value.strip()
                )
                self.parent.users_data[i].email = (
                    self.edit_user_email_field.value.strip()
                )
                self.parent.users_data[i].password = (
                    self.edit_user_password_field.value.strip()
                )
                self.parent.users_data[i].role_id = int(
                    self.edit_user_role_dropdown.value
                )
                break

        # TODO: Appel API pour mettre à jour l'utilisateur
        # success = await self.parent.services.update_user(updated_user)

        self._close_user_edit_dialog()
        await self.parent.tables.update_user_table()

    async def _save_classroom_changes(self, e):
        """Sauvegarder les modifications classe"""
        if not self.edit_classroom_name_field.value:
            return

        # Mettre à jour les données localement
        for i, classroom in enumerate(self.parent.classrooms_data):
            if classroom.id_classroom == self.current_editing_classroom_id:
                self.parent.classrooms_data[i].name = (
                    self.edit_classroom_name_field.value.strip()
                )
                self.parent.classrooms_data[i].level = (
                    self.edit_classroom_level_field.value.strip()
                )
                break

        # TODO: Appel API pour mettre à jour la classe
        # success = await self.parent.services.update_classroom(updated_classroom)

        self._close_classroom_edit_dialog()
        await self.parent.tables.update_classroom_table()

    async def _save_school_year_changes(self, e):
        """Sauvegarder les modifications année scolaire"""
        if not self.edit_school_year_name_field.value:
            return

        # Mettre à jour les données localement
        for i, school_year in enumerate(self.parent.school_year_data):
            if school_year.id_school_year == self.current_editing_school_year_id:
                self.parent.school_year_data[i].name = (
                    self.edit_school_year_name_field.value.strip()
                )
                self.parent.school_year_data[i].start_date = (
                    self.edit_school_year_start_date_field.value.strip()
                )
                self.parent.school_year_data[i].end_date = (
                    self.edit_school_year_end_date_field.value.strip()
                )
                self.parent.school_year_data[i].is_active = (
                    self.edit_school_year_status_switch.value
                )
                break

        # TODO: Appel API pour mettre à jour l'année scolaire
        # success = await self.parent.services.update_school_year(updated_school_year)

        self._close_school_year_edit_dialog()
        await self.parent.tables.update_school_year_table()

    async def _save_staff_changes(self, e):
        """Sauvegarder les modifications personnel"""
        if not self.edit_staff_first_name_field.value:
            return
        if not self.edit_staff_salary_field.value:
            return

        # Mettre à jour les données localement
        for i, staff in enumerate(self.parent.staff_data):
            if staff.id_staff == self.current_editing_staff_id:
                self.parent.staff_data[i].first_name = (
                    self.edit_staff_first_name_field.value.strip()
                )
                self.parent.staff_data[i].last_name = (
                    self.edit_staff_last_name_field.value.strip()
                )
                self.parent.staff_data[i].position = (
                    self.edit_staff_position_field.value.strip()
                )
                self.parent.staff_data[i].hire_date = (
                    self.edit_staff_hire_date_field.value.strip()
                )
                self.parent.staff_data[i].salary_base = float(
                    self.edit_staff_salary_field.value
                )
                break

        # TODO: Appel API pour mettre à jour le personnel
        # success = await self.parent.services.update_staff(updated_staff)

        self._close_staff_edit_dialog()
        await self.parent.tables.update_staff_table()

    #################################################################
    # MÉTHODES D'OUVERTURE DES DIALOGUES DE SUPPRESSION
    #################################################################

    def open_user_delete_dialog(self, user: UserModel):
        """Ouvrir le dialogue de suppression utilisateur"""
        if not user:
            return

        self.current_deleting_user_id = user.id_user
        self.user_name_to_be_deleted.value = user.username
        self.delete_user_motive_field.value = ""

        self.parent.page.show_dialog(self.delete_user_dialog)
        self.parent.page.update()

    def open_classroom_delete_dialog(self, classroom: ClassroomModel):
        """Ouvrir le dialogue de suppression classe"""
        if not classroom:
            return

        self.current_deleting_classroom_id = classroom.id_classroom
        self.classroom_name_to_be_deleted.value = classroom.name
        self.delete_classroom_motive_field.value = ""

        self.parent.page.show_dialog(self.delete_classroom_dialog)
        self.parent.page.update()

    def open_school_year_delete_dialog(self, school_year: SchoolYearModel):
        """Ouvrir le dialogue de suppression année scolaire"""
        if not school_year:
            return

        self.current_deleting_school_year_id = school_year.id_school_year
        self.school_year_name_to_be_deleted.value = school_year.name
        self.delete_school_year_motive_field.value = ""

        self.parent.page.show_dialog(self.delete_school_year_dialog)
        self.parent.page.update()

    def open_staff_delete_dialog(self, staff: StaffModel):
        """Ouvrir le dialogue de suppression personnel"""
        if not staff:
            return

        self.current_deleting_staff_id = staff.id_staff
        full_name = f"{staff.first_name} {staff.last_name}"
        self.staff_name_to_be_deleted.value = full_name
        self.delete_staff_motive_field.value = ""

        self.parent.page.show_dialog(self.delete_staff_dialog)
        self.parent.page.update()

    #################################################################
    # MÉTHODES DE FERMETURE DES DIALOGUES DE SUPPRESSION
    #################################################################

    def _close_user_delete_dialog(self, e=None):
        """Fermer le dialogue de suppression utilisateur"""
        self.delete_user_dialog.open = False
        self.parent.page.update()

    def _close_classroom_delete_dialog(self, e=None):
        """Fermer le dialogue de suppression classe"""
        self.delete_classroom_dialog.open = False
        self.parent.page.update()

    def _close_school_year_delete_dialog(self, e=None):
        """Fermer le dialogue de suppression année scolaire"""
        self.delete_school_year_dialog.open = False
        self.parent.page.update()

    def _close_staff_delete_dialog(self, e=None):
        """Fermer le dialogue de suppression personnel"""
        self.delete_staff_dialog.open = False
        self.parent.page.update()

    #################################################################
    # MÉTHODES DE CONFIRMATION DE SUPPRESSION
    #################################################################

    async def _confirm_delete_user(self, e):
        """Confirmer la suppression utilisateur"""
        if (
            not self.delete_user_motive_field.value
            or not self.delete_user_motive_field.value.strip()
        ):
            return

        # Supprimer des données locales
        self.parent.users_data = [
            u
            for u in self.parent.users_data
            if u.id_user != self.current_deleting_user_id
        ]

        # TODO: Appel API pour supprimer l'utilisateur
        # success = await self.parent.services.delete_user(self.current_deleting_user_id, motive)

        self._close_user_delete_dialog()
        await self.parent.tables.update_user_table()

    async def _confirm_delete_classroom(self, e):
        """Confirmer la suppression classe"""
        if (
            not self.delete_classroom_motive_field.value
            or not self.delete_classroom_motive_field.value.strip()
        ):
            return

        # Supprimer des données locales
        self.parent.classrooms_data = [
            c
            for c in self.parent.classrooms_data
            if c.id_classroom != self.current_deleting_classroom_id
        ]

        # TODO: Appel API pour supprimer la classe
        # success = await self.parent.services.delete_classroom(self.current_deleting_classroom_id, motive)

        self._close_classroom_delete_dialog()
        await self.parent.tables.update_classroom_table()

    async def _confirm_delete_school_year(self, e):
        """Confirmer la suppression année scolaire"""
        if (
            not self.delete_school_year_motive_field.value
            or not self.delete_school_year_motive_field.value.strip()
        ):
            return

        # Supprimer des données locales
        self.parent.school_year_data = [
            sy
            for sy in self.parent.school_year_data
            if sy.id_school_year != self.current_deleting_school_year_id
        ]

        # TODO: Appel API pour supprimer l'année scolaire
        # success = await self.parent.services.delete_school_year(self.current_deleting_school_year_id, motive)

        self._close_school_year_delete_dialog()
        await self.parent.tables.update_school_year_table()

    async def _confirm_delete_staff(self, e):
        """Confirmer la suppression personnel"""
        if (
            not self.delete_staff_motive_field.value
            or not self.delete_staff_motive_field.value.strip()
        ):
            return

        # Supprimer des données locales
        self.parent.staff_data = [
            s
            for s in self.parent.staff_data
            if s.id_staff != self.current_deleting_staff_id
        ]

        # TODO: Appel API pour supprimer le personnel
        # success = await self.parent.services.delete_staff(self.current_deleting_staff_id, motive)

        self._close_staff_delete_dialog()
        await self.parent.tables.update_staff_table()

    #################################################################
    # MÉTHODES UTILITAIRES
    #################################################################

    def _populate_roles_dropdown_for_edit(self):
        """Peupler le dropdown des rôles pour l'édition"""
        self.edit_user_role_dropdown.options = [
            DropdownOption(key="1", text="Administrateur"),
            DropdownOption(key="2", text="Enseignant"),
            DropdownOption(key="3", text="Comptable"),
            DropdownOption(key="4", text="Surveillant"),
        ]
