from flet import *  # type: ignore
from core import AppState, Constants
from utils import Utils
import asyncio
from .students_services import StudentsServices


class StudentsScreen:
    def __init__(self, app_state: AppState, page: Page):
        self.app_state = app_state
        self.translations = app_state.translations
        self.services = StudentsServices(app_state)
        self.page = page

        self.build_components()

    async def on_mount(self):
        self.translations = self.app_state.translations
        await asyncio.sleep(1)  # Yield control to the event loop

    def get_text(self, key: str) -> str:
        return self.app_state.translations.get(key, key)

    @staticmethod
    def get_box_style() -> dict:
        return {
            "border_radius": BorderRadius.all(10),
            "shadow": BoxShadow(color="black12", blur_radius=5, offset=Offset(0, 2)),
            "bgcolor": "#f8faff",
        }

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

    def build(self) -> Control:
        return Column(
            horizontal_alignment=CrossAxisAlignment.STRETCH,
            controls=[
                Container(
                    content=Row(
                        controls=[
                            Text(
                                value=self.get_text("students_management"),
                                size=24,
                                weight=FontWeight.BOLD,
                                color=Constants.PRIMARY_COLOR,
                            ),
                            IconButton(
                                icon=Icons.REFRESH,
                                icon_color=Constants.PRIMARY_COLOR,
                                tooltip=self.get_text("refresh"),
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
