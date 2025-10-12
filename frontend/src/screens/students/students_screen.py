from json import load
from math import e, exp
from flet import *  # type: ignore
from core import AppState, Constants
from utils import Utils
import asyncio
from .students_services import StudentsServices
from models import ClassroomModel


class StudentsScreen:
    def __init__(self, app_state: AppState, page: Page):
        self.app_state = app_state
        self.translations = app_state.translations
        self.services = StudentsServices(app_state)
        self.page = page

        self.build_components()
        self._build_add_form_components()

    async def on_mount(self):
        self.translations = self.app_state.translations
        await self.load_data()

    def refresh_students_data(self, e):
        self.main_content.content = self.loading_indicator
        self.main_content.update()
        asyncio.create_task(self.load_data())

    def get_text(self, key: str) -> str:
        return self.app_state.translations.get(key, key)

    def propagate_classrooms(self, classrooms: list[ClassroomModel]):
        options = [
            DropdownOption(key=str(c.id_classroom), text=c.name) for c in classrooms
        ]
        self.classroom_form.options = options

    async def load_data(self):
        students_status, students_data = await self.services.load_students_data()
        classrooms_status, classrooms_data = await self.services.load_classrooms_data()
        # students_per_classroom_status, students_per_classroom_data = (
        #     await self.services.load_students_per_classroom_data()
        # )
        # await asyncio.sleep(2)  # Simuler un délai de chargement
        self.main_content.content = Column(
            expand=True,
            horizontal_alignment=CrossAxisAlignment.STRETCH,
            scroll=ScrollMode.AUTO,
            controls=[
                Row(
                    # scroll=ScrollMode.AUTO,
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    spacing=20,
                    controls=[
                        self.create_stat_card(
                            title=self.get_text("total_students"),
                            value=str(len(students_data)) if students_status else "N/A",
                            icon=Icons.SCHOOL,
                            color=Constants.PRIMARY_COLOR,
                        ),
                        self.create_stat_card(
                            title=self.get_text("total_classrooms"),
                            value=(
                                str(len(classrooms_data))
                                if classrooms_status
                                else "N/A"
                            ),
                            icon=Icons.CLASS_,
                            color=Constants.SECONDARY_COLOR,
                        ),
                        self.create_stat_card(
                            title=self.get_text("average_students_per_classroom"),
                            value=(
                                str(round(len(students_data) / len(classrooms_data), 2))
                                if students_status
                                and classrooms_status
                                and len(classrooms_data) > 0
                                else "N/A"
                            ),
                            icon=Icons.GROUP,
                            color=Colors.ORANGE,
                        ),
                    ],
                ),
                self.container_form,
                Container(
                    content=Text(
                        self.get_text("students_list"),
                        size=18,
                        weight=FontWeight.BOLD,
                        color=Constants.PRIMARY_COLOR,
                    ),
                    margin=Margin(top=20, bottom=10),
                    expand=True,
                ),
            ],
        )
        if classrooms_status:
            self.propagate_classrooms(classrooms_data)
        try:
            self.main_content.update()
        except Exception as e:
            # print("Error updating main content:", e)
            pass

    @staticmethod
    def get_box_style() -> dict:
        return {
            "border_radius": BorderRadius.all(10),
            "shadow": BoxShadow(color="black12", blur_radius=5, offset=Offset(0, 2)),
            "bgcolor": "#f8faff",
        }

    def _build_add_form_components(self):
        self.full_name_field_form = TextField(
            label=self.get_text("full_name"),
            hint_text=self.get_text("enter_full_name"),
            autofocus=True,
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=2,
            helper=self.get_text("full_name_helper"),
        )

        self.birth_date_field_form = TextField(
            label=self.get_text("birth_date"),
            hint_text=self.get_text("enter_birth_date"),
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            keyboard_type=KeyboardType.DATETIME,
            value="01-01-2000",
            expand=1,
            helper=self.get_text("date_format_dd_mm_yyyy"),
        )

        self.classroom_form = Dropdown(
            label=self.get_text("classroom"),
            border_radius=BorderRadius.all(5),
            options=[],
            expand=1,
            helper_text=self.get_text("select_classroom"),
            width=float("inf"),
        )

        self.button_submit_form = Button(
            content=self.get_text("submit"),
            icon=Icons.SAVE,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                bgcolor=Constants.PRIMARY_COLOR,
                padding=Padding(10, 20, 10, 20),
                color="white",
            ),
        )

        self.button_cancel_form = Button(
            content=self.get_text("cancel"),
            icon=Icons.CANCEL,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                bgcolor=Constants.CANCEL_COLOR,
                padding=Padding(10, 20, 10, 20),
                color="white",
            ),
            on_click=self._close_add_form,
        )

        self.container_form = Container(
            content=Column(
                horizontal_alignment=CrossAxisAlignment.STRETCH,
                controls=[
                    Text(
                        value=self.get_text("add_student"),
                        style=TextStyle(
                            size=18,
                            weight=FontWeight.BOLD,
                            color=Constants.PRIMARY_COLOR,
                        ),
                    ),
                    Row(
                        controls=[
                            self.full_name_field_form,
                            self.birth_date_field_form,
                            self.classroom_form,
                        ],
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        # wrap=True,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        # expand=True,
                    ),
                    Row(
                        controls=[
                            self.button_submit_form,
                            self.button_cancel_form,
                        ],
                        alignment=MainAxisAlignment.END,
                    ),
                ],
            ),
            visible=False,
            padding=Padding.all(15),
            margin=Margin(top=20),
            **self.get_box_style(),
        )

    def _clear_form(self):
        self.full_name_field_form.value = ""
        self.birth_date_field_form.value = "01-01-2000"
        if self.classroom_form.options:
            self.classroom_form.value = self.classroom_form.options[0].key
        self.full_name_field_form.update()
        self.birth_date_field_form.update()
        self.classroom_form.update()

    def _open_add_form(self, e):
        self.container_form.visible = True
        self.add_button.icon = Icons.CLOSE
        self.add_button.tooltip = self.get_text("close_form")
        self.add_button.content = self.get_text("close_form")
        self.add_button.style.bgcolor = Constants.CANCEL_COLOR
        self.add_button.on_click = self._close_add_form
        self.add_button.update()
        self.container_form.update()

    def _close_add_form(self, e):
        self.container_form.visible = False
        self.add_button.icon = Icons.ADD
        self.add_button.style.bgcolor = Constants.PRIMARY_COLOR
        self.add_button.tooltip = self.get_text("add_student")
        self.add_button.content = self.get_text("add_student")
        self.add_button.on_click = self._open_add_form
        self._clear_form()
        self.add_button.update()
        self.container_form.update()

    def create_stat_card(
        self, title: str, value: str, icon: str, color: str, subtitle: str = None
    ) -> Control:
        """Créer une carte de statistique améliorée"""
        return Container(
            content=Row(
                controls=[
                    Icon(icon, color=color, size=30),
                    Column(
                        controls=[
                            Text(title, size=14, color=Colors.GREY_600, no_wrap=False),
                            Text(value, size=20, weight=FontWeight.BOLD),
                        ],
                        spacing=0,
                    ),
                ],
                alignment=MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=Padding.all(15),
            expand=1,
            # width=250,
            height=100,
            **self.get_box_style(),
        )

    def build_components(self):
        self.loading_indicator = CupertinoActivityIndicator(
            animating=True, color=Constants.PRIMARY_COLOR, radius=50
        )

        self.add_button = Button(
            icon=Icons.ADD,
            tooltip=self.get_text("add_student"),
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                bgcolor=Constants.PRIMARY_COLOR,
                padding=Padding(10, 20, 10, 20),
                color="white",
            ),
            on_click=self._open_add_form,
            content=self.get_text("add_student"),
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
                            Row(
                                controls=[
                                    self.add_button,
                                    IconButton(
                                        icon=Icons.REFRESH,
                                        icon_color=Constants.PRIMARY_COLOR,
                                        tooltip=self.get_text("refresh"),
                                        on_click=self.refresh_students_data,
                                    ),
                                ],
                                spacing=10,
                                alignment=MainAxisAlignment.END,
                                vertical_alignment=CrossAxisAlignment.CENTER,
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
