from flet import *  # type: ignore
from typing import Callable

from core import AppState, Constants


class Page5:
    """Page 5 — Prêt à commencer"""

    def __init__(self, appState: AppState, to_next_page: Callable) -> None:
        self.app_state = appState
        self.to_next_page = to_next_page
        self.on_mount()

    def on_mount(self):
        self.translations = self.app_state.translations

    def get_text(self, key: str):
        return self.translations.get(key, "XXXXXXXXXXX")

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
                                src="assets/images/page5.png", fit=BoxFit.COVER
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
                                    self.get_text("page5title"),
                                    style=TextStyle(
                                        size=20,
                                        weight=FontWeight.BOLD,
                                        color=Constants.PRIMARY_COLOR,
                                    ),
                                ),
                                Container(expand=True),
                                Text(self.get_text("page5content")),
                                Row(
                                    controls=[
                                        OutlinedButton(
                                            content=self.get_text("previous"),
                                            on_click=lambda e: self.to_next_page(4),
                                        ),
                                        Button(
                                            content=self.get_text("startnow"),
                                            on_click=lambda e: self.to_next_page(6),
                                            bgcolor=Constants.PRIMARY_COLOR,
                                            color="white",
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
