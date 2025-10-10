from flet import *  # type: ignore
import asyncio

from core import AppState, Constants
from utils import StorageUtils
from typing import Callable, Awaitable
from .login_services import LoginServices

from screens.welcome.welcome_screen import WelcomeScreen


class LoginScreen:
    def __init__(
        self,
        appState: AppState,
        on_login_success: Callable | Awaitable,
        on_change_language: Callable,
        page: Page | None = None,
        is_first_launch: bool = True,
    ) -> None:
        self.on_login_success = on_login_success
        self.app_state = appState
        self.on_change_language = on_change_language
        self.page = page
        self.is_first_launch = is_first_launch

        self.on_mount()

    def on_mount(self):
        self.translations = self.app_state.translations
        self.login_services = LoginServices()
        self._build_components()

    def set_page(self, page: Page):
        self.page = page

    def _build_components(self):
        self.user_name_field = TextField(
            label=self.get_text("username"),
            hint_text=self.get_text("usernamehint"),
            prefix_icon=Icons.PERSON_OUTLINE,
            autofocus=True,
            on_submit=self.on_login,
        )
        self.password_field = TextField(
            label=self.get_text("password"),
            hint_text=self.get_text("passwordhint"),
            password=True,
            can_reveal_password=True,
            prefix_icon=Icons.LOCK_OUTLINE,
            on_submit=self.on_login,
        )

        self.login_button = Button(
            content=self.get_text("login"),
            icon=Icons.LOGIN,
            style=ButtonStyle(
                bgcolor=Constants.PRIMARY_COLOR,
                color="white",
                shape=RoundedRectangleBorder(radius=10),
            ),
            height=50,
            on_click=self.on_login,
        )

        self.error_text = Text(
            value=self.get_text("invalid"), color="red", visible=False
        )

        self.menu_language = Dropdown(
            text="Français" if self.app_state.current_language == "fr" else "English",
            label="Langue" if self.app_state.current_language == "fr" else "Language",
            options=[
                DropdownOption(key="fr", text="Français"),
                DropdownOption(key="en", text="English"),
            ],
            align=Alignment.BOTTOM_RIGHT,
            margin=Margin.only(right=20, bottom=20),
            on_change=self.change_language,
        )
        self.main_content = Container(
            height=400,
            width=400,
            expand=False,
            expand_loose=True,
            padding=Padding.symmetric(horizontal=40, vertical=20),
            border_radius=20,
            shadow=BoxShadow(spread_radius=1, blur_radius=10, color=Colors.BLACK26),
            bgcolor=Colors.with_opacity(1, Constants.BACKGROUND_COLOR),
            align=Alignment.CENTER,
            content=Column(
                expand=False,
                expand_loose=True,
                controls=[
                    Text(
                        self.get_text("connexion"),
                        style=TextStyle(size=20, weight=FontWeight.BOLD),
                        text_align=TextAlign.CENTER,
                    ),
                    Container(height=20),
                    self.user_name_field,
                    self.password_field,
                    self.error_text,
                    self.login_button,
                    TextButton(
                        content=self.get_text("newuser"),
                    ),
                ],
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.STRETCH,
            ),
        )

        self.welcome_screen = WelcomeScreen(self.app_state, self.change_page)

        # Détermine quel contenu afficher
        # Si l'utilisateur est connecté : afficher main_content
        # Si c'est la première ouverture : afficher welcome_screen
        # Sinon : afficher main_content (écran de connexion)
        if self.app_state.is_logged_in:
            initial_content = self.main_content
        elif self.is_first_launch:
            initial_content = self.welcome_screen.build_page()
        else:
            initial_content = self.main_content

        self.container = Container(
            content=initial_content,
            alignment=Alignment.CENTER,
            expand=True,
        )

    def on_login(self, e: Event):
        username = self.user_name_field.value
        password = self.password_field.value
        self.error_text.visible = False
        self.error_text.update()

        if not username:
            self.user_name_field.error = self.get_text("usernameerror")
            self.user_name_field.update()
            return
        self.user_name_field.error = None
        self.user_name_field.update()
        if not password:
            self.password_field.error = self.get_text("passworderror")
            self.password_field.update()
            return
        self.password_field.error = None
        self.password_field.update()
        result = self.login_services.authenticate(username, password)
        if not result:
            self.error_text.visible = True
            self.error_text.update()
            return
        self.app_state.current_user = result
        self.on_login_success(self.app_state)

    def reset_login_form(self):
        self.user_name_field.value = ""
        self.password_field.value = ""
        self.user_name_field.error = None
        self.password_field.error = None
        self.user_name_field.update()
        self.password_field.update()

    def change_language(self, e: Event):
        if e.control.value:
            self.on_change_language(e.control.value)

    def change_page(self):
        self.container.content = self.main_content
        # Marquer que l'application a été ouverte au moins une fois
        asyncio.run_coroutine_threadsafe(
            StorageUtils.save_to_local_storage(
                self.page, Constants.STORAGE_KEY_FIRST_LAUNCH, "false"
            ),
            asyncio.get_event_loop(),
        ).add_done_callback(lambda f: print("first_launch saved to local storage"))
        self.container.update()

    def get_text(self, key: str):
        return self.translations.get(key, "Xxxxxxxxxxxxx")

    def build_page(self) -> Control:
        return Stack(
            fit=StackFit.PASS_THROUGH,
            alignment=Alignment.CENTER,
            align=Alignment.CENTER,
            expand=True,
            controls=[
                Container(
                    expand=True,  # type: ignore
                    align=Alignment.CENTER_LEFT,
                    foreground_decoration=BoxDecoration(
                        bgcolor=Constants.PRIMARY_COLOR,
                        border_radius=BorderRadius.only(bottom_right=1000),
                    ),
                ),
                CircleAvatar(
                    bgcolor="white",
                    radius=150,
                    align=Alignment.TOP_CENTER,
                    offset=Offset(0, -0.5),
                    content=Text(
                        self.get_text("title"),
                        style=TextStyle(
                            color=Constants.PRIMARY_COLOR,
                            size=30,
                            weight=FontWeight.BOLD,
                        ),
                        align=Alignment.BOTTOM_CENTER,
                        margin=Margin.only(bottom=50),
                    ),
                ),
                self.container,
                self.menu_language,
            ],
        )
