from flet import *  # type: ignore
from typing import Callable

from core import AppState
from .pages.page1 import Page1
from .pages.page2 import Page2
from .pages.page3 import Page3
from .pages.page4 import Page4
from .pages.page5 import Page5


class WelcomeScreen:
    def __init__(self, appState: AppState, go_to_next_page: Callable) -> None:
        self.app_state = appState
        self.go_to_next_page = go_to_next_page
        self.on_mount()

    def _build_components(self):
        self.page1 = Page1(self.app_state, self.to_next_page)
        self.page2 = Page2(self.app_state, self.to_next_page)
        self.page3 = Page3(self.app_state, self.to_next_page)
        self.page4 = Page4(self.app_state, self.to_next_page)
        self.page5 = Page5(self.app_state, self.to_next_page)
        self.animated_switcher = AnimatedSwitcher(
            duration=Duration(seconds=1),
            transition=AnimatedSwitcherTransition.FADE,
            content=self.page1.build_page(),
            reverse_duration=Duration(seconds=1),
            switch_in_curve=AnimationCurve.EASE_IN,
            switch_out_curve=AnimationCurve.EASE_OUT,
        )
        self.main_page = Container(content=self.animated_switcher)

    def on_mount(self):
        self.translations = self.app_state.translations
        self._build_components()

    def set_page(self, page: Page):
        self.page = page

    def get_text(self, key: str) -> str:
        return self.translations.get(key, key)

    def to_next_page(self, page_number: int):
        if page_number == 1:
            self.animated_switcher.content = self.page1.build_page()
        elif page_number == 2:
            self.animated_switcher.content = self.page2.build_page()
        elif page_number == 3:
            self.animated_switcher.content = self.page3.build_page()
        elif page_number == 4:
            self.animated_switcher.content = self.page4.build_page()
        elif page_number == 5:
            self.animated_switcher.content = self.page5.build_page()
        elif page_number == 6:
            self.go_to_next_page()
        self.main_page.update()

    def build_page(self) -> Control:
        return self.main_page
