from flet import *  # type: ignore
from typing import Callable

from core import AppState, Constants


class Page1:
    """Page 1 — Bienvenue sur iSchool"""

    def __init__(self, appState: AppState, to_next_page: Callable) -> None:
        self.app_state = appState
        self.to_next_page = to_next_page
        self.on_mount()

    def on_mount(self):
        self.translations = self.app_state.translations

    def get_text(self, key: str):
        return self.translations.get(key, "Xxxxxxxxxxxxx")

    def build_page(self) -> Control:
        return Container(
            height=400,
            width=650,
            expand=False,
            expand_loose=True,
            border_radius=20,
            shadow=BoxShadow(spread_radius=1, blur_radius=10, color=Colors.BLACK26),
            bgcolor=Colors.with_opacity(1, Constants.BACKGROUND_COLOR),
            align=Alignment.CENTER,
            content=Row(
                controls=[
                    Container(
                        bgcolor="white",
                        expand=1,
                        foreground_decoration=BoxDecoration(
                            image=DecorationImage(
                                src="assets/images/page1.png", fit=BoxFit.COVER
                            )
                        ),
                    ),
                    Container(
                        bgcolor="white",
                        expand=1,
                        padding=Padding.all(30),
                        content=Column(
                            controls=[
                                Container(height=20),
                                Text(
                                    self.get_text("page1title"),
                                    style=TextStyle(
                                        size=20,
                                        weight=FontWeight.BOLD,
                                        color=Constants.PRIMARY_COLOR,
                                    ),
                                ),
                                Container(expand=True),
                                Text(self.get_text("page1content")),
                                Row(
                                    controls=[
                                        OutlinedButton(
                                            content=self.get_text("start_tour"),
                                            on_click=lambda e: self.to_next_page(2),
                                        ),
                                    ],
                                    alignment=MainAxisAlignment.END,
                                ),
                            ],
                            alignment=MainAxisAlignment.CENTER,
                            horizontal_alignment=CrossAxisAlignment.START,
                        ),
                    ),
                ],
                expand=True,
                alignment=MainAxisAlignment.CENTER,
                vertical_alignment=CrossAxisAlignment.STRETCH,
            ),
        )
