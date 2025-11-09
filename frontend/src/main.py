import asyncio
from flet import *  # type: ignore

"""Application principale - iSchool"""
# import asyncio

# Imports des modules locaux
from core import AppState, Constants
from screens import (
    LoginScreen,
    DashboardScreen,
    StudentsScreen,
    PaymentScreen,
    AdminScreen,
    CheckoutScreen,
)
from models import UserModel


class MainAppp:
    def __init__(self, page: Page, is_logged_in: bool, is_first_launch: bool) -> None:
        self.page: Page = page
        self.app_state = AppState()
        self.app_state.is_logged_in = is_logged_in
        self.is_first_launch = is_first_launch
        self.translations = self.app_state.translations

        self._load_screens()

    def _load_screens(self, is_language_change: bool = False):
        self.login_screen = LoginScreen(
            appState=self.app_state,
            on_login_success=self.on_login_success,
            on_change_language=self.change_language,
            page=self.page,
            is_first_launch=self.is_first_launch,
        )
        # self.login_screen.set_page(self.page)
        self.dashboard_screen = DashboardScreen(
            appState=self.app_state,
            page=self.page,
        )

        self.students_screen = StudentsScreen(
            app_state=self.app_state,
            page=self.page,
        )

        self.payment_screen = PaymentScreen(
            app_state=self.app_state,
            page=self.page,
        )

        self.checkout_screen = CheckoutScreen(
            appState=self.app_state,
            page=self.page,
        )

        self.admin_screen = AdminScreen(app_state=self.app_state, page=self.page)

        if not is_language_change:
            # self._setup_screen(self.login_screen.build_page())
            # For testing purposes, directly show main layout
            self.app_state.current_user = UserModel(
                id_user=1,
                username="admin",
                email="admin@example.com",
                password="admin",
                role_id=1,
            )
            self.on_login_success(self.app_state)

    def _setup_screen(self, screen: Control):

        self.page.controls.clear()
        self.page.bgcolor = "white"
        self.page.controls = [SafeArea(content=screen, expand=True)]

    def get_text(self, key: str):
        return self.app_state.translations.get(key, key)

    def on_logout(self, e):
        self.app_state.current_user = None
        self.page.update()
        self._load_screens()

    def on_login_success(self, app_state: AppState):
        self.app_state = app_state
        self.init_ui_components()
        self.show_main_layout()

    def change_language(self, language: str):
        self.app_state.current_language = language
        self.app_state.translations = self.app_state.load_translations(language)
        self.translations = self.app_state.translations
        self._load_screens()

    def change_home_language(self, e: Event):
        self.app_state.current_language = e.control.value
        self.app_state.translations = self.app_state.load_translations(e.control.value)
        self.translations = self.app_state.translations
        self.init_ui_components()
        self._load_screens(is_language_change=True)
        self.show_main_layout()

    def init_ui_components(self):
        """Initialiser les composants UI"""

        # Menu langue
        self.menu_language = Dropdown(
            text=Constants.AVAILABLE_LANGUAGES.get(
                self.app_state.current_language, "Français"
            ),
            label=self.get_text("language"),
            options=[
                DropdownOption(key=k, text=Constants.AVAILABLE_LANGUAGES.get(k))
                for k in Constants.AVAILABLE_LANGUAGES.keys()
            ],
            align=Alignment.CENTER_LEFT,
            margin=Margin.only(right=20, bottom=20),
            on_change=self.change_home_language,
            dense=True,
            menu_style=MenuStyle(alignment=Alignment.CENTER_LEFT),
        )

        # Barre de navigation
        self.navigation_rail = NavigationRail(
            height=self.page.height * 2,
            selected_index=0,
            label_type=NavigationRailLabelType.ALL,
            extended=True,
            min_width=100,
            min_extended_width=200,
            leading=FloatingActionButton(
                icon=Icons.MENU,
                mini=True,
                on_click=self.toggle_navigation,
                tooltip=self.get_text("menu"),
            ),
            group_alignment=-0.9,
            destinations=self.get_navigation_destinations(),
            on_change=self.on_navigation_change,
            visible=True,
            elevation=2,
            bgcolor=Constants.PRIMARY_COLOR,
            indicator_color=Colors.WHITE,
            selected_label_text_style=TextStyle(
                color=Colors.WHITE, size=16, weight=FontWeight.BOLD
            ),
            unselected_label_text_style=TextStyle(color=Colors.WHITE, size=14),
            expand_loose=True,
        )

        # Barre d'application
        self.app_bar = AppBar(
            title=Text(Constants.APP_NAME, weight=FontWeight.BOLD),
            center_title=True,
            bgcolor=Constants.PRIMARY_COLOR,
            color=Colors.WHITE,
            actions=[
                IconButton(
                    icon=Icons.NOTIFICATIONS,
                    tooltip=self.get_text("notifications"),
                    # on_click=self.show_notifications,
                ),
                IconButton(
                    icon=Icons.BRIGHTNESS_6,
                    tooltip=self.get_text("changetheme"),
                    on_click=self.toggle_theme,
                ),
                PopupMenuButton(
                    items=[
                        PopupMenuItem(
                            content=f"{self.get_text('connected')}: {self.app_state.current_user.username if self.app_state.current_user else self.get_text('invite')}",
                            icon=Icons.PERSON,
                            disabled=True,
                        ),
                        PopupMenuItem(),  # Séparateur
                        PopupMenuItem(
                            content=self.get_text("profile"),
                            icon=Icons.ACCOUNT_CIRCLE,
                            # on_click=self.show_profile,
                        ),
                        PopupMenuItem(
                            content=self.menu_language,
                            icon=Icons.LANGUAGE,
                        ),
                        PopupMenuItem(
                            content=self.get_text("deconnexion"),
                            icon=Icons.LOGOUT,
                            on_click=self.on_logout,
                        ),
                    ]
                ),
            ],
            visible=True,
        )

        # Zone de contenu principal
        self.content_area = Container(
            expand=True,
            # expand_loose=True,
            # height=self.page.height,
            # padding=padding.all(20),
            # margin=margin.only(bottom=20),
        )

    def get_navigation_destinations(self):
        """Obtenir les destinations de navigation selon les permissions"""
        destinations = []

        # Tableau de bord (toujours visible)
        destinations.append(
            NavigationRailDestination(
                icon=Icon(
                    Icons.DASHBOARD,
                    color=Colors.WHITE,
                    tooltip=self.get_text("dashboard"),
                ),
                selected_icon=Icons.DASHBOARD,
                label=self.get_text("dashboard"),
                tooltip=self.get_text("dashboard"),
                data="dashboard",
            )
        )

        # Élèves
        destinations.append(
            NavigationRailDestination(
                icon=Icon(
                    Icons.PEOPLE, color=Colors.WHITE, tooltip=self.get_text("students")
                ),
                selected_icon=Icons.PEOPLE,
                label=self.get_text("students"),
                tooltip=self.get_text("students"),
                data="students",
            )
        )

        # Paiements
        destinations.append(
            NavigationRailDestination(
                icon=Icon(
                    Icons.PAYMENT, color=Colors.WHITE, tooltip=self.get_text("payments")
                ),
                selected_icon=Icons.PAYMENT,
                label=self.get_text("payments"),
                tooltip=self.get_text("payments"),
                data="payments",
            )
        )

        # Caisse
        destinations.append(
            NavigationRailDestination(
                icon=Icon(
                    Icons.ACCOUNT_BALANCE_WALLET,
                    color=Colors.WHITE,
                    tooltip=self.get_text("checkout"),
                ),
                selected_icon=Icons.ACCOUNT_BALANCE_WALLET,
                label=self.get_text("checkout"),
                tooltip=self.get_text("checkout"),
                data="checkout",
            )
        )

        # Rapports
        destinations.append(
            NavigationRailDestination(
                icon=Icon(
                    Icons.ASSESSMENT,
                    color=Colors.WHITE,
                    tooltip=self.get_text("reports"),
                ),
                selected_icon=Icons.ASSESSMENT,
                label=self.get_text("reports"),
                tooltip=self.get_text("reports"),
                data="reports",
            )
        )

        # Administration
        destinations.append(
            NavigationRailDestination(
                icon=Icon(
                    Icons.ADMIN_PANEL_SETTINGS,
                    color=Colors.WHITE,
                    tooltip=self.get_text("admin"),
                ),
                selected_icon=Icons.ADMIN_PANEL_SETTINGS,
                label=self.get_text("admin"),
                tooltip=self.get_text("admin"),
                data="admin",
            )
        )

        return destinations

    def show_main_layout(self):
        """Afficher la mise en page principale"""
        self.content_area.content = self.dashboard_screen.build()
        asyncio.create_task(self.dashboard_screen.on_mount())

        main_layout = Row(
            controls=[
                self.navigation_rail,
                VerticalDivider(width=1),
                Container(content=self.content_area, expand=True, padding=20),
            ],
            expand=True,
            vertical_alignment=CrossAxisAlignment.START,
            spacing=0,
            expand_loose=True,
        )

        self.page.controls.clear()
        self.page.add(
            SafeArea(
                content=Column(
                    controls=[
                        self.app_bar,
                        Container(content=main_layout, expand=True),
                    ],
                    spacing=0,
                    horizontal_alignment=CrossAxisAlignment.STRETCH,
                ),
                expand=True,
                minimum_padding=Padding.all(0),
            )
        )
        self.page.update()

    def on_navigation_change(self, e: Event):
        """Gérer le changement de navigation"""
        index = e.control.selected_index
        destinations = self.get_navigation_destinations()

        if index >= len(destinations):
            return

        selected_data = destinations[index].data

        if selected_data == "dashboard":
            self.content_area.content = self.dashboard_screen.build()
            # self.content_area.content = self.dashboard_screen.build()
            # asyncio.create_task(self.dashboard_screen.on_mount())

        elif selected_data == "students":
            self.content_area.content = self.students_screen.build()
            asyncio.create_task(self.students_screen.on_mount())

        elif selected_data == "payments":
            self.content_area.content = self.payment_screen.build()
            asyncio.create_task(self.payment_screen.on_mount())

        elif selected_data == "checkout":
            self.content_area.content = self.checkout_screen.build()

        elif selected_data == "reports":
            self.content_area.content = Container(
                content=Text("Gestion des Rapports en cours de développement")
            )

        elif selected_data == "admin":
            self.content_area.content = self.admin_screen.build()
            asyncio.create_task(self.admin_screen.on_mount())

        self.content_area.update()

    def toggle_navigation(self, e):
        """Basculer l'état de la navigation"""
        self.navigation_rail.extended = not getattr(
            self.navigation_rail, "extended", False
        )
        self.navigation_rail.label_type = (
            NavigationRailLabelType.ALL
            if self.navigation_rail.extended
            else NavigationRailLabelType.NONE
        )
        self.navigation_rail.update()

    def toggle_theme(self, e):
        """Basculer le thème"""
        if self.app_state.theme_mode == ThemeMode.LIGHT:
            self.app_state.theme_mode = ThemeMode.DARK
        else:
            self.app_state.theme_mode = ThemeMode.LIGHT

        self.page.theme_mode = self.app_state.theme_mode
        self.page.update()

    # async def show_notifications(self, e):
    #     """Afficher les notifications"""
    #     if self.app_state.notifications:
    #         for notification in self.app_state.notifications:
    #             try:
    #                 self.notification_banner.show(
    #                     notification["message"], notification["type"]
    #                 )
    #             except Exception:
    #                 pass
    #         self.app_state.clear_notifications()
    #     else:
    #         try:
    #             self.notification_banner.show("Aucune nouvelle notification", "info")
    #         except Exception:
    #             try:
    #                 self.notification_banner.close_banner(None)
    #             except Exception:
    #                 pass
    #     # close the notification banner after showing notifications
    #     await self.notification_banner.close_banner_after(Config.CLOSE_BANNER_TIME)


async def main(page: Page):
    # # Vérifier si l'utilisateur est connecté
    # is_logged_in = await StorageUtils.get_from_local_storage(
    #     page, Constants.STORAGE_KEY_IS_LOGGED_IN
    # )

    # # Vérifier si c'est la première ouverture de l'application
    # first_launch_value = await StorageUtils.get_from_local_storage(
    #     page, Constants.STORAGE_KEY_FIRST_LAUNCH
    # )

    # # Si la clé n'existe pas, c'est la première ouverture
    # is_first_launch = first_launch_value is None or first_launch_value != "false"
    is_logged_in = False  # For testing purposes
    is_first_launch = False  # For testing purposes

    # print(f"is_logged_in: {is_logged_in}")
    # print(f"is_first_launch: {is_first_launch}")

    page.padding = 0
    page.title = Constants.APP_NAME + f" v{Constants.VERSION}"
    app = MainAppp(page, is_logged_in, is_first_launch)
    page.update()


if __name__ == "__main__":
    run(main)
