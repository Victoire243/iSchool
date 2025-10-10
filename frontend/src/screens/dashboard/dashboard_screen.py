from flet import *  # type: ignore
from flet_charts import (
    BarChart,
    BarChartGroup,
    BarChartRod,
    ChartAxis,
    ChartAxisLabel,
)
from core import AppState, Constants
from utils import Utils
import asyncio
from .dashboard_services import DashboardServices


class DashboardScreen:
    def __init__(self, appState: AppState, page: Page | None = None) -> None:
        self.app_state = appState
        self.page = page
        self.dashboard_services = DashboardServices(self.app_state)

        # Call on_mount as async task
        self.build_components()

    async def on_mount(self):
        self.translations = self.app_state.translations
        status, result = await self.dashboard_services.load_dashboard_summery()
        if status:
            self.load_data(result)
        else:
            self.main_content.content = Text("Error loading data")
            try:
                self.main_content.update()
            except Exception as e:
                print(f"Error updating main content: {e}")

    def refresh_dashboard(self, e):
        self.main_content.content = self.loading_indicator
        self.main_content.update()
        asyncio.create_task(self.on_mount())

    def load_data(self, result: dict):
        self.total_students = result.get("total_students", 0)
        self.total_payments = result.get("total_payments", 0)
        self.total_expenses = result.get("total_expenses", 0)
        self.amount_payments = result.get("amount_payments", 0.0)
        self.amount_expenses = result.get("amount_expenses", 0.0)
        self.cash_balance = result.get("cash_balance", 0.0)
        self.active_school_year = result.get("active_school_year", "None")
        self.students_per_classroom = result.get("students_per_classroom", {})
        self.main_content.content = Column(
            controls=[
                Container(
                    content=ListTile(
                        leading=Icon(
                            icon=Icons.CALENDAR_MONTH,
                            color=Constants.PRIMARY_COLOR,
                            size=30,
                        ),
                        title=self.active_school_year,
                        subtitle=self.get_text("active_school_year"),
                        title_text_style=TextStyle(
                            size=20,
                            weight=FontWeight.BOLD,
                            color=Constants.SECONDARY_COLOR,
                        ),
                    ),
                    padding=Padding.symmetric(vertical=10),
                    **self.get_box_style(),
                ),
                Row(
                    controls=[
                        self.create_stat_card(
                            title=self.get_text("total_students"),
                            value=str(self.total_students),
                            icon=Icons.SCHOOL,
                            color=Colors.BLUE,
                        ),
                        self.create_stat_card(
                            title=self.get_text("total_payments"),
                            value=str(self.total_payments),
                            icon=Icons.PAYMENT,
                            color=Colors.GREEN,
                        ),
                        self.create_stat_card(
                            title=self.get_text("total_expenses"),
                            value=f"{self.total_expenses:,.1f}",
                            icon=Icons.MONEY_OFF,
                            color=Colors.BROWN,
                        ),
                        self.create_stat_card(
                            title=self.get_text("amount_payments"),
                            value=f"${self.amount_payments:,.2f}",
                            icon=Icons.ATTACH_MONEY,
                            color=Colors.ORANGE,
                        ),
                        self.create_stat_card(
                            title=self.get_text("amount_expenses"),
                            value=f"${self.amount_expenses:,.2f}",
                            icon=Icons.MONEY_OFF,
                            color=Colors.RED,
                        ),
                        self.create_stat_card(
                            title=self.get_text("cash_balance"),
                            value=f"${self.cash_balance:,.2f}",
                            icon=Icons.ACCOUNT_BALANCE_WALLET,
                            color=Colors.PURPLE,
                        ),
                    ],
                    wrap=True,
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    spacing=20,
                ),
                Container(
                    padding=Padding.symmetric(vertical=10),
                    content=Row(
                        controls=[
                            self.get_bar_graph_for_students_per_class(
                                self.students_per_classroom
                            ),
                            Container(width=10),  # Spacer
                            Container(
                                expand=2,
                                padding=Padding.all(10),
                                content=Column(
                                    controls=[
                                        Text(
                                            self.get_text("students_per_classroom"),
                                            size=20,
                                            weight=FontWeight.BOLD,
                                            color=Constants.PRIMARY_COLOR,
                                        ),
                                        Divider(),
                                        ListView(
                                            expand=True,
                                            spacing=5,
                                            padding=Padding.all(0),
                                            auto_scroll=True,
                                            scroll=ScrollMode.AUTO,
                                            controls=[
                                                ListTile(
                                                    leading=CircleAvatar(
                                                        content=Text(
                                                            str(i + 1),
                                                            color=Colors.WHITE,
                                                        ),
                                                        bgcolor=Constants.PRIMARY_COLOR,
                                                    ),
                                                    title=Text(
                                                        Utils.trunc_text(class_name),
                                                        weight=FontWeight.BOLD,
                                                    ),
                                                    trailing=Text(
                                                        f"{count} {self.get_text('students')}",
                                                        weight=FontWeight.BOLD,
                                                        color=Constants.SECONDARY_COLOR,
                                                    ),
                                                )
                                                for i, (class_name, count) in enumerate(
                                                    self.students_per_classroom.items()
                                                )
                                            ],
                                        ),
                                    ]
                                ),
                            ),
                        ]
                    ),
                    **self.get_box_style(),
                ),
            ],
            spacing=20,
            expand=True,
            scroll=ScrollMode.AUTO,
            horizontal_alignment=CrossAxisAlignment.STRETCH,
        )
        try:
            self.main_content.update()
        except Exception as e:
            print(f"Error updating main content: {e}")

    def get_bar_graph_for_students_per_class(self, data: dict) -> Control:
        return BarChart(
            groups=[
                BarChartGroup(
                    x=i,
                    rods=[
                        BarChartRod(
                            from_y=0,
                            to_y=count,
                            width=40,
                            color=Constants.PRIMARY_COLOR,
                            border_radius=0,
                            tooltip=f"{class_name}: {count} {self.get_text('students')}",
                        )
                    ],
                )
                for i, (class_name, count) in enumerate(data.items())
            ],
            border=Border.all(width=1, color=Colors.BLACK12),
            left_axis=ChartAxis(
                label_size=30,
                title=Text(self.get_text("students"), weight=FontWeight.BOLD),
                title_size=20,
            ),
            bottom_axis=ChartAxis(
                labels=[
                    ChartAxisLabel(value=i, label=Utils.trunc_text(class_name))
                    for i, (class_name, count) in enumerate(data.items())
                ],
                title=Text(self.get_text("classrooms"), weight=FontWeight.BOLD),
            ),
            margin=Margin.all(10),
            expand=3,
        )

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
                            Text(title, size=14, color=Colors.GREY_600),
                            Text(value, size=20, weight=FontWeight.BOLD),
                        ],
                        spacing=0,
                    ),
                ],
                alignment=MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=Padding.all(15),
            width=250,
            height=100,
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
                                value=self.get_text("dashboard"),
                                size=24,
                                weight=FontWeight.BOLD,
                                color=Constants.PRIMARY_COLOR,
                            ),
                            IconButton(
                                icon=Icons.REFRESH,
                                icon_color=Constants.PRIMARY_COLOR,
                                tooltip=self.get_text("refresh"),
                                on_click=self.refresh_dashboard,
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
