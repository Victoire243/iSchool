"""
Admin Tables Module
Contains all table-related components and logic
"""

from flet import *  # type: ignore
from core import Constants
from utils import Utils
from models import UserModel, ClassroomModel, SchoolYearModel, StaffModel, FeeModel


class AdminTables:
    """Manages all data tables for admin entities"""

    def __init__(self, parent):
        """
        Initialize tables with reference to parent AdminScreen
        Args:
            parent: Reference to AdminScreen instance
        """
        self.parent = parent

    # ========================================================================
    # USERS TABLE
    # ========================================================================

    def create_users_table_header(self):
        """Create table header row"""
        return Container(
            content=Row(
                controls=[
                    Container(
                        content=Text(
                            self.parent.get_text("username"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.parent.get_text("email"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=3,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.parent.get_text("password"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.parent.get_text("role"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=1,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.parent.get_text("actions"),
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

    async def create_user_table_row(self, user: UserModel, index):
        """Create a table row for a user"""
        user_name = user.username
        user_email = user.email
        user_password = user.password
        user_role = await self.parent.services.get_user_role_by_user_id(user.id_user)

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
                        bgcolor=self.parent.get_color_by_user_role(user_role),
                        border_radius=BorderRadius.all(10),
                    ),
                    Container(
                        content=Row(
                            controls=[
                                IconButton(
                                    icon=Icons.EDIT,
                                    icon_color=Constants.PRIMARY_COLOR,
                                    tooltip=self.parent.get_text("edit"),
                                    on_click=lambda e, u=user: self.parent._open_user_edit_dialog(
                                        u
                                    ),
                                ),
                                IconButton(
                                    icon=Icons.DELETE,
                                    icon_color=Constants.CANCEL_COLOR,
                                    tooltip=self.parent.get_text("delete"),
                                    on_click=lambda e, u=user: self.parent._open_user_delete_dialog(
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

    async def update_user_table(self):
        """Update the users table with current data"""
        # Build table content
        table_controls = [self.create_users_table_header()]

        # Update add button
        self.parent.add_action_button.content = self.parent.get_text("new_user")

        if not self.parent.users_data:
            table_controls.append(
                Container(
                    content=Column(
                        controls=[
                            Icon(Icons.SEARCH_OFF, size=60, color=Colors.GREY_400),
                            Text(
                                self.parent.get_text("no_users_found"),
                                size=18,
                                weight=FontWeight.BOLD,
                                color=Colors.GREY_600,
                            ),
                            Text(
                                self.parent.get_text("no_students_message"),
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
            for index, user in enumerate(self.parent.users_data):
                table_controls.append(await self.create_user_table_row(user, index))

        self.parent.data_table_container.content = Column(
            controls=table_controls,
            scroll=ScrollMode.AUTO,
            spacing=0,
        )

        try:
            self.parent.add_action_button.update()
            self.parent.data_table_container.update()
        except Exception as e:
            pass

    # ========================================================================
    # CLASSROOMS TABLE
    # ========================================================================

    def create_classrooms_table_header(self):
        """Create classrooms table header row"""
        return Container(
            content=Row(
                controls=[
                    Container(
                        content=Text(
                            self.parent.get_text("classroom"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=3,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.parent.get_text("level"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=3,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.parent.get_text("actions"),
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

    def create_classroom_table_row(self, classroom: ClassroomModel, index):
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
                                    tooltip=self.parent.get_text("edit"),
                                    on_click=lambda e, c=classroom: self.parent._open_classroom_edit_dialog(
                                        c
                                    ),
                                ),
                                IconButton(
                                    icon=Icons.DELETE,
                                    icon_color=Constants.CANCEL_COLOR,
                                    tooltip=self.parent.get_text("delete"),
                                    on_click=lambda e, c=classroom: self.parent._open_classroom_delete_dialog(
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

    async def update_classroom_table(self):
        """Update the classrooms table with current data"""
        table_controls = [self.create_classrooms_table_header()]
        self.parent.add_action_button.content = self.parent.get_text("new_classroom")

        if not self.parent.classrooms_data:
            table_controls.append(
                Container(
                    content=Column(
                        controls=[
                            Icon(Icons.SEARCH_OFF, size=60, color=Colors.GREY_400),
                            Text(
                                self.parent.get_text("no_classrooms_found"),
                                size=18,
                                weight=FontWeight.BOLD,
                                color=Colors.GREY_600,
                            ),
                            Text(
                                self.parent.get_text("no_classrooms_message"),
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
            for index, classroom in enumerate(self.parent.classrooms_data):
                table_controls.append(self.create_classroom_table_row(classroom, index))

        self.parent.data_table_container.content = Column(
            controls=table_controls,
            scroll=ScrollMode.AUTO,
            spacing=0,
        )

        try:
            self.parent.add_action_button.update()
            self.parent.data_table_container.update()
        except Exception as e:
            pass

    # ========================================================================
    # SCHOOL YEARS TABLE
    # ========================================================================

    def create_school_years_table_header(self):
        """Create school years table header row"""
        return Container(
            content=Row(
                controls=[
                    Container(
                        content=Text(
                            self.parent.get_text("name"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.parent.get_text("start_date"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.parent.get_text("end_date"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.parent.get_text("is_active"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.parent.get_text("actions"),
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

    def create_school_year_table_row(self, school_year: SchoolYearModel, index):
        """Create a table row for a school year"""
        row_color = "#f8faff" if index % 2 == 0 else "#ffffff"

        return Container(
            content=Row(
                controls=[
                    Container(
                        content=Text(school_year.name, size=14),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(school_year.start_date, size=14),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(school_year.end_date, size=14),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Switch(
                            value=school_year.is_active,
                            disabled=school_year.is_active,
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
                                    tooltip=self.parent.get_text("edit"),
                                    on_click=lambda e, sy=school_year: self.parent._open_school_year_edit_dialog(
                                        sy
                                    ),
                                ),
                                IconButton(
                                    icon=Icons.DELETE,
                                    icon_color=Constants.CANCEL_COLOR,
                                    tooltip=self.parent.get_text("delete"),
                                    on_click=lambda e, sy=school_year: self.parent._open_school_year_delete_dialog(
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

    async def update_school_year_table(self):
        """Update the school year table with current data"""
        table_controls = [self.create_school_years_table_header()]
        self.parent.add_action_button.content = self.parent.get_text("new_school_year")

        if not self.parent.school_year_data:
            table_controls.append(
                Container(
                    content=Column(
                        controls=[
                            Icon(Icons.SEARCH_OFF, size=60, color=Colors.GREY_400),
                            Text(
                                self.parent.get_text("no_school_years_found"),
                                size=18,
                                weight=FontWeight.BOLD,
                                color=Colors.GREY_600,
                            ),
                            Text(
                                self.parent.get_text("no_school_years_message"),
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
            for index, school_year in enumerate(self.parent.school_year_data):
                table_controls.append(
                    self.create_school_year_table_row(school_year, index)
                )

        self.parent.data_table_container.content = Column(
            controls=table_controls,
            scroll=ScrollMode.AUTO,
            spacing=0,
        )

        try:
            self.parent.add_action_button.update()
            self.parent.data_table_container.update()
        except Exception as e:
            pass

    # ========================================================================
    # STAFF TABLE
    # ========================================================================

    def create_staff_table_header(self):
        """Create staff table header row"""
        return Container(
            content=Row(
                controls=[
                    Container(
                        content=Text(
                            self.parent.get_text("full_name"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=3,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.parent.get_text("position"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.parent.get_text("hire_date"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.parent.get_text("salary_base"),
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.parent.get_text("actions"),
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

    def create_staff_table_row(self, staff: StaffModel, index):
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
                                    tooltip=self.parent.get_text("edit"),
                                    on_click=lambda e, s=staff: self.parent._open_staff_edit_dialog(
                                        s
                                    ),
                                ),
                                IconButton(
                                    icon=Icons.DELETE,
                                    icon_color=Constants.CANCEL_COLOR,
                                    tooltip=self.parent.get_text("delete"),
                                    on_click=lambda e, s=staff: self.parent._open_staff_delete_dialog(
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

    async def update_staff_table(self):
        """Update the staff table with current data"""
        table_controls = [self.create_staff_table_header()]
        self.parent.add_action_button.content = self.parent.get_text("new_staff")

        if not self.parent.staff_data:
            table_controls.append(
                Container(
                    content=Column(
                        controls=[
                            Icon(Icons.SEARCH_OFF, size=60, color=Colors.GREY_400),
                            Text(
                                self.parent.get_text("no_staff_found"),
                                size=18,
                                weight=FontWeight.BOLD,
                                color=Colors.GREY_600,
                            ),
                            Text(
                                self.parent.get_text("no_staff_message"),
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
            for index, staff in enumerate(self.parent.staff_data):
                table_controls.append(self.create_staff_table_row(staff, index))

        self.parent.data_table_container.content = Column(
            controls=table_controls,
            scroll=ScrollMode.AUTO,
            spacing=0,
        )

        try:
            self.parent.add_action_button.update()
            self.parent.data_table_container.update()
        except Exception as e:
            pass

    # ========================================================================
    # FEES TABLE
    # ========================================================================

    def create_fees_table_header(self):
        """Create table header row for fees"""
        return Container(
            content=Row(
                controls=[
                    Container(
                        content=Text(
                            "Nom",
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            "Description",
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=3,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            "Montant",
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=1,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            "Périodicité",
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            "Statut",
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        expand=1,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.parent.get_text("actions"),
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

    def create_fee_table_row(self, fee: FeeModel, index):
        """Create a table row for a fee"""
        row_color = "#f8faff" if index % 2 == 0 else "#ffffff"

        # Map periodicity to display text
        periodicity_map = {
            "monthly": "Mensuel",
            "quarterly": "Trimestriel",
            "semester": "Semestriel",
            "annual": "Annuel",
            "one_time": "Unique",
        }
        periodicity_display = periodicity_map.get(fee.periodicity, fee.periodicity)

        status_color = Colors.GREEN if fee.is_active else Colors.GREY_400
        status_text = "Actif" if fee.is_active else "Inactif"

        return Container(
            content=Row(
                controls=[
                    Container(
                        content=Text(fee.name, size=14, weight=FontWeight.W_500),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            Utils.trunc_text(fee.description, length=40),
                            size=14,
                        ),
                        expand=3,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            f"{fee.amount:.2f} $",
                            size=14,
                            weight=FontWeight.BOLD,
                            color=Constants.PRIMARY_COLOR,
                        ),
                        expand=1,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Container(
                            content=Text(
                                periodicity_display,
                                size=12,
                                color=Colors.WHITE,
                            ),
                            padding=Padding.symmetric(horizontal=10, vertical=5),
                            bgcolor=Constants.SECONDARY_COLOR,
                            border_radius=BorderRadius.all(10),
                        ),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Container(
                            content=Text(
                                status_text,
                                size=12,
                                color=Colors.WHITE,
                            ),
                            padding=Padding.symmetric(horizontal=10, vertical=5),
                            bgcolor=status_color,
                            border_radius=BorderRadius.all(10),
                        ),
                        expand=1,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Row(
                            controls=[
                                IconButton(
                                    icon=Icons.EDIT,
                                    icon_color=Constants.PRIMARY_COLOR,
                                    tooltip=self.parent.get_text("edit"),
                                    on_click=lambda e, f=fee: self.parent._open_fee_edit_dialog(
                                        f
                                    ),
                                ),
                                IconButton(
                                    icon=Icons.DELETE,
                                    icon_color=Constants.CANCEL_COLOR,
                                    tooltip=self.parent.get_text("delete"),
                                    on_click=lambda e, f=fee: self.parent._open_fee_delete_dialog(
                                        f
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

    async def update_fee_table(self):
        """Update the fee table with current data"""
        table_controls = [self.create_fees_table_header()]
        self.parent.add_action_button.content = "Nouveau frais"

        if not self.parent.fees_data:
            table_controls.append(
                Container(
                    content=Column(
                        controls=[
                            Icon(Icons.SEARCH_OFF, size=60, color=Colors.GREY_400),
                            Text(
                                "Aucun frais trouvé",
                                size=18,
                                weight=FontWeight.BOLD,
                                color=Colors.GREY_600,
                            ),
                            Text(
                                "Ajoutez des frais pour commencer",
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
            for index, fee in enumerate(self.parent.fees_data):
                table_controls.append(self.create_fee_table_row(fee, index))

        self.parent.data_table_container.content = Column(
            controls=table_controls,
            scroll=ScrollMode.AUTO,
            spacing=0,
        )

        try:
            self.parent.add_action_button.update()
            self.parent.data_table_container.update()
        except Exception as e:
            pass
