"""
Admin Screen - Modular Version
===============================
Version modulaire utilisant des fichiers séparés pour chaque fonctionnalité.

Modules utilisés:
- admin_components.py : Composants UI réutilisables
- admin_forms.py : Gestion des formulaires
- admin_form_handlers.py : Logique de soumission des formulaires
- admin_tables.py : Gestion des tables de données
- admin_dialogs.py : Gestion des dialogues (à créer)
"""

from flet import *  # type: ignore
import asyncio
from core import AppState, Constants
from .admin_services import AdminServices
from .admin_components import AdminComponents
from .admin_forms import AdminForms
from .admin_form_handlers import AdminFormHandlers
from .admin_tables import AdminTables
from .admin_dialogs import AdminDialogs
from models import UserModel, ClassroomModel, SchoolYearModel, StaffModel, FeeModel


class AdminScreen:
    """
    Écran d'administration principal (Version modulaire).
    Délègue les fonctionnalités spécifiques à des modules dédiés.
    """

    def __init__(self, app_state: AppState, page: Page):
        self.app_state = app_state
        self.page = page
        self.services = AdminServices(app_state)

        # Initialize data structures
        self.users_data = []
        self.classrooms_data = []
        self.staff_data = []
        self.school_year_data = []
        self.fees_data = []

        # Initialize modules
        self.forms = AdminForms(self)
        self.form_handlers = AdminFormHandlers(self)
        self.tables = AdminTables(self)
        self.dialogs = AdminDialogs(self)

        # Build UI components
        self.build_components()
        self._build_table_components()
        self.dialogs.build_all_dialogs()  # Build all edit and delete dialogs

    # ========================================================================
    # LIFECYCLE METHODS
    # ========================================================================

    async def on_mount(self):
        """Called when the screen is mounted"""
        await self.load_data()

    def refresh_admin_data(self, e):
        """Refresh all admin data"""
        self.main_content.content = self.loading_indicator
        self.main_content.update()
        asyncio.create_task(self.load_data())

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def get_text(self, key: str) -> str:
        """Get translated text for a given key"""
        return self.app_state.translations.get(key, key)

    @staticmethod
    def get_box_style() -> dict:
        """Return common box styling"""
        return AdminComponents.get_box_style()

    @staticmethod
    def get_color_by_user_role(role: str) -> ColorValue:
        """Get color based on user role"""
        return AdminComponents.get_color_by_user_role(role)

    # ========================================================================
    # DATA LOADING
    # ========================================================================

    async def load_data(self):
        """Load all necessary data for the admin screen"""
        try:
            # Load data in parallel
            (
                (users_status, users_data),
                (classrooms_status, classrooms_data),
                (staff_status, staff_data),
                (school_year_status, school_year_data),
                (fees_status, fees_data),
            ) = await asyncio.gather(
                self.services.load_users_data(),
                self.services.load_classrooms_data(),
                self.services.load_staff_data(),
                self.services.load_school_years_data(),
                self.services.load_fees_data(),
                return_exceptions=True,
            )

            # Store data
            self.users_data = users_data if users_status else []
            self.classrooms_data = classrooms_data if classrooms_status else []
            self.staff_data = staff_data if staff_status else []
            self.school_year_data = school_year_data if school_year_status else []
            self.fees_data = fees_data if fees_status else []

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
                            AdminComponents.create_stat_card(
                                title=self.get_text("total_users"),
                                value=str(total_users),
                                icon=Icons.PEOPLE,
                                color=Constants.PRIMARY_COLOR,
                            ),
                            AdminComponents.create_stat_card(
                                title=self.get_text("total_classrooms"),
                                value=str(total_classrooms),
                                icon=Icons.CLASS_,
                                color=Constants.SECONDARY_COLOR,
                            ),
                            AdminComponents.create_stat_card(
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

            # Update appropriate table based on active menu
            match self.active_menu.value:
                case "classrooms":
                    await self.tables.update_classroom_table()
                case "users":
                    await self.tables.update_user_table()
                case "school_years":
                    await self.tables.update_school_year_table()
                case "staff":
                    await self.tables.update_staff_table()
                case "fees":
                    await self.tables.update_fee_table()

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
                DropdownOption(
                    key="fees",
                    text="Gestion des frais",
                    leading_icon=Icons.PAYMENTS,
                    data="fees",
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
        """Handle when user changes the active menu"""
        match e.control.value:
            case "classrooms":
                await self.tables.update_classroom_table()
            case "users":
                await self.tables.update_user_table()
            case "school_years":
                await self.tables.update_school_year_table()
            case "staff":
                await self.tables.update_staff_table()
            case "fees":
                await self.tables.update_fee_table()

        try:
            self.main_content.update()
        except Exception as ex:
            print(f"Error updating main content: {ex}")

    def _build_table_components(self):
        """Build table container"""
        self.data_table_container = Container(
            content=Column(
                controls=[],
                scroll=ScrollMode.AUTO,
            ),
            padding=Padding.all(10),
            **self.get_box_style(),
        )

    # ========================================================================
    # FORM MANAGEMENT
    # ========================================================================

    def _open_form(self, e):
        """Open the appropriate form based on active menu"""
        active_menu = self.active_menu.value

        # Set the appropriate form in add_container
        if active_menu == "users":
            self.add_container.content = self.user_form_container
            self.forms.populate_roles_dropdown()
        elif active_menu == "classrooms":
            self.add_container.content = self.classroom_form_container
        elif active_menu == "school_years":
            self.add_container.content = self.school_year_form_container
        elif active_menu == "staff":
            self.add_container.content = self.staff_form_container
        elif active_menu == "fees":
            self.add_container.content = self.fee_form_container

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

        self.forms.clear_all_forms()

        self.add_container.update()
        self.add_action_button.update()

    # ========================================================================
    # FORM SUBMISSION HANDLERS (Delegated to form_handlers module)
    # ========================================================================

    async def _submit_user_form(self, e):
        """Submit user form"""
        await self.form_handlers.submit_user_form(e)

    async def _submit_classroom_form(self, e):
        """Submit classroom form"""
        await self.form_handlers.submit_classroom_form(e)

    async def _submit_school_year_form(self, e):
        """Submit school year form"""
        await self.form_handlers.submit_school_year_form(e)

    async def _submit_staff_form(self, e):
        """Submit staff form"""
        await self.form_handlers.submit_staff_form(e)

    async def _submit_fee_form(self, e):
        """Submit fee form"""
        await self.form_handlers.submit_fee_form(e)

    # ========================================================================
    # TABLE UPDATE METHODS (Delegated to tables module)
    # ========================================================================

    async def _update_user_table(self):
        """Update users table"""
        await self.tables.update_user_table()

    async def _update_classroom_table(self):
        """Update classrooms table"""
        await self.tables.update_classroom_table()

    async def _update_school_year_table(self):
        """Update school years table"""
        await self.tables.update_school_year_table()

    async def _update_staff_table(self):
        """Update staff table"""
        await self.tables.update_staff_table()

    # ========================================================================
    # EDIT & DELETE DIALOGS - Delegated to admin_dialogs.py
    # ========================================================================

    def _build_edit_dialogs(self):
        """Build all edit dialogs - DEPRECATED: Use dialogs.build_all_dialogs()"""
        self.dialogs.build_all_dialogs()

    def _open_user_edit_dialog(self, user):
        """Open user edit dialog"""
        self.dialogs.open_user_edit_dialog(user)

    def _open_classroom_edit_dialog(self, classroom):
        """Open classroom edit dialog"""
        self.dialogs.open_classroom_edit_dialog(classroom)

    def _open_school_year_edit_dialog(self, school_year):
        """Open school year edit dialog"""
        self.dialogs.open_school_year_edit_dialog(school_year)

    def _open_staff_edit_dialog(self, staff):
        """Open staff edit dialog"""
        self.dialogs.open_staff_edit_dialog(staff)

    def _open_fee_edit_dialog(self, fee):
        """Open fee edit dialog"""
        self.dialogs.open_fee_edit_dialog(fee)

    def _open_user_delete_dialog(self, user):
        """Open user delete dialog"""
        self.dialogs.open_user_delete_dialog(user)

    def _open_classroom_delete_dialog(self, classroom):
        """Open classroom delete dialog"""
        self.dialogs.open_classroom_delete_dialog(classroom)

    def _open_school_year_delete_dialog(self, school_year):
        """Open school year delete dialog"""
        self.dialogs.open_school_year_delete_dialog(school_year)

    def _open_staff_delete_dialog(self, staff):
        """Open staff delete dialog"""
        self.dialogs.open_staff_delete_dialog(staff)

    def _open_fee_delete_dialog(self, fee):
        """Open fee delete dialog"""
        self.dialogs.open_fee_delete_dialog(fee)

    # ========================================================================
    # MAIN BUILD METHOD
    # ========================================================================

    def build(self) -> Column:
        """Build the main admin screen layout"""
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

    # ========================================================================
    # SERVICE CALLBACKS
    # ========================================================================

    async def _activate_school_year(self, e: Event):
        """Activate a school year"""
        pass
