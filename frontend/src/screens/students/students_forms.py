from flet import *
from core import Constants
from .students_components import StudentsComponents


class StudentsForms:
    def __init__(self, students_screen):
        self.screen = students_screen

    def build_add_form_components(self):
        self.screen.full_name_field_form = TextField(
            label=self.screen.get_text("full_name"),
            hint_text=self.screen.get_text("enter_full_name"),
            autofocus=True,
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=2,
            helper=self.screen.get_text("full_name_helper"),
        )

        self.screen.birth_date_field_form = TextField(
            label=self.screen.get_text("birth_date"),
            hint_text=self.screen.get_text("enter_birth_date"),
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            keyboard_type=KeyboardType.DATETIME,
            value="01-01-2000",
            expand=1,
            helper=self.screen.get_text("date_format_dd_mm_yyyy"),
        )

        self.screen.classroom_form = Dropdown(
            label=self.screen.get_text("classroom"),
            border_radius=BorderRadius.all(5),
            options=[],
            expand=1,
            helper_text=self.screen.get_text("select_classroom"),
            width=float("inf"),
            menu_width=200,
        )

        self.screen.gender_form = Dropdown(
            label=self.screen.get_text("gender"),
            border_radius=BorderRadius.all(5),
            options=[
                DropdownOption(key="M", text=self.screen.get_text("male")),
                DropdownOption(key="F", text=self.screen.get_text("female")),
            ],
            expand=1,
            helper_text=self.screen.get_text("select_gender"),
            width=float("inf"),
            menu_width=150,
        )

        self.screen.address_field_form = TextField(
            label=self.screen.get_text("address"),
            hint_text=self.screen.get_text("enter_address"),
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=2,
            helper=self.screen.get_text("address_helper"),
            multiline=True,
        )

        self.screen.parent_contact_field_form = TextField(
            label=self.screen.get_text("parent_contact"),
            hint_text=self.screen.get_text("enter_parent_contact"),
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=2,
            helper=self.screen.get_text("parent_contact_helper"),
            multiline=True,
        )

        self.screen.button_submit_form = Button(
            content=self.screen.get_text("submit"),
            icon=Icons.SAVE,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                bgcolor=Constants.PRIMARY_COLOR,
                padding=Padding(10, 20, 10, 20),
                color="white",
            ),
            on_click=self.screen.form_handlers.submit_add_form,
        )

        self.screen.button_cancel_form = Button(
            content=self.screen.get_text("cancel"),
            icon=Icons.CANCEL,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                bgcolor=Constants.CANCEL_COLOR,
                padding=Padding(10, 20, 10, 20),
                color="white",
            ),
            on_click=self.screen.form_handlers.close_add_form,
        )

        self.screen.container_form = Container(
            content=Column(
                horizontal_alignment=CrossAxisAlignment.STRETCH,
                controls=[
                    Text(
                        value=self.screen.get_text("add_student"),
                        style=TextStyle(
                            size=18,
                            weight=FontWeight.BOLD,
                            color=Constants.PRIMARY_COLOR,
                        ),
                    ),
                    Row(
                        controls=[
                            self.screen.full_name_field_form,
                            self.screen.birth_date_field_form,
                            self.screen.classroom_form,
                        ],
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                    ),
                    Row(
                        controls=[
                            self.screen.gender_form,
                            self.screen.address_field_form,
                            self.screen.parent_contact_field_form,
                        ],
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                    ),
                    Row(
                        controls=[
                            self.screen.button_submit_form,
                            self.screen.button_cancel_form,
                        ],
                        alignment=MainAxisAlignment.END,
                    ),
                ],
            ),
            visible=False,
            padding=Padding.all(15),
            margin=Margin(top=20),
            **StudentsComponents.get_box_style(),
        )

    def build_load_from_file_dialog(self):
        self.screen.classroom_load_file_from = Dropdown(
            label=self.screen.get_text("classroom"),
            border_radius=BorderRadius.all(5),
            options=[],
        )
