import asyncio
from flet import *  # type: ignore

"""Application principale - iSchool"""
# import asyncio

# Imports des modules locaux
from core import Config
from core import AppState
from screens import LoginScreen
from utils import StorageUtils


class MainAppp:
    def __init__(self, page: Page, is_logged_in: bool) -> None:
        self.page: Page = page
        self.app_state = AppState()
        self.app_state.is_logged_in = is_logged_in

        self._load_screens()

    def _load_screens(self):
        self.login_screen = LoginScreen(
            appState=self.app_state,
            on_login_success=self.on_login_success,
            on_change_language=self.change_language,
            page=self.page,
        )
        # self.login_screen.set_page(self.page)
        self._setup_screen(self.login_screen.build_page())

    def _setup_screen(self, screen: Control):

        self.page.controls.clear()
        self.page.padding = 0
        self.page.bgcolor = "white"
        self.page.controls = [SafeArea(content=screen, expand=True)]

    def on_login_success(self):
        pass

    def change_language(self, language: str):
        self.app_state.current_language = language
        self.app_state.translations = self.app_state.load_translations(language)
        self._load_screens()


async def main(page: Page):
    is_logged_in = await StorageUtils.get_from_local_storage(page, "is_logged_in")
    print(f"is_logged_in: {is_logged_in}")
    app = MainAppp(page, is_logged_in)
    page.update()


if __name__ == "__main__":
    asyncio.run(run_async(main))
