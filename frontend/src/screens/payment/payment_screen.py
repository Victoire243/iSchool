from re import U
from flet import *  # type: ignore
from core import AppState, Constants
from utils import Utils
from models import (
    StudentModel,
    ClassroomModel,
    EnrollmentModel,
    PaymentModel,
    PaymentTypeModel,
)
from .payment_services import PaymentServices
import asyncio
from datetime import datetime


class PaymentScreen:
    def __init__(self, app_state: AppState, page: Page):
        self.app_state = app_state
        self.page = page
        self.services = PaymentServices(app_state)

        # Data storage
        self.students_data = []
        self.classrooms_data = []
        self.enrollments_data = []
        self.payments_data = []
        self.payment_types_data = []
        self.filtered_payments = []

        # Selection state
        self.selected_student_id = None

        # Pagination and filters
        self.current_page = 1
        self.items_per_page = 10
        self.search_query = ""
        self.selected_payment_type_filter = "all"

        self.build_components()
        self._build_add_form_components()
        self._build_table_components()

    def get_text(self, key: str) -> str:
        return self.app_state.translations.get(key, key)

    @staticmethod
    def get_box_style() -> dict:
        return {
            "border_radius": BorderRadius.all(10),
            "shadow": BoxShadow(color="black12", blur_radius=5, offset=Offset(0, 2)),
            "bgcolor": "#f8faff",
        }

    async def on_mount(self):
        """Called when the screen is mounted"""
        await self.load_data()

    def refresh_payments_data(self, e):
        """Refresh all payment data"""
        self.main_content.content = self.loading_indicator
        self.main_content.update()
        asyncio.create_task(self.load_data())

    async def load_data(self):
        """Load all necessary data for the payment screen"""
        try:
            # Load data in parallel
            students_status, students_data = await self.services.load_students_data()
            classrooms_status, classrooms_data = (
                await self.services.load_classrooms_data()
            )
            enrollments_status, enrollments_data = (
                await self.services.load_enrollments_data()
            )
            payments_status, payments_data = await self.services.load_payments_data()
            payment_types_status, payment_types_data = (
                await self.services.load_payment_types_data()
            )

            # Store data
            self.students_data = students_data if students_status else []
            self.classrooms_data = classrooms_data if classrooms_status else []
            self.enrollments_data = enrollments_data if enrollments_status else []
            self.payments_data = payments_data if payments_status else []
            self.payment_types_data = payment_types_data if payment_types_status else []

            # Reset filters
            self.current_page = 1
            self.search_query = ""
            self.search_field.value = ""
            self.selected_payment_type_filter = "all"

            # Update payment type filter options
            self._update_payment_type_filter_options()
            if hasattr(self, "payment_type_filter_dropdown"):
                self.payment_type_filter_dropdown.value = "all"

            # Apply filters
            self._apply_filters()

            # Calculate statistics
            total_payments = len(self.payments_data)
            total_amount = sum(p.amount for p in self.payments_data)
            avg_payment = total_amount / total_payments if total_payments > 0 else 0

            # Update main content with stats and table
            self.main_content.content = Column(
                expand=True,
                horizontal_alignment=CrossAxisAlignment.STRETCH,
                scroll=ScrollMode.AUTO,
                controls=[
                    Row(
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        spacing=20,
                        controls=[
                            self.create_stat_card(
                                title=self.get_text("total_payments"),
                                value=str(total_payments),
                                icon=Icons.PAYMENT,
                                color=Constants.PRIMARY_COLOR,
                            ),
                            self.create_stat_card(
                                title=self.get_text("total_amount"),
                                value=f"{total_amount:,.0f} FC",
                                icon=Icons.ATTACH_MONEY,
                                color=Constants.SECONDARY_COLOR,
                            ),
                            self.create_stat_card(
                                title=self.get_text("average_payment"),
                                value=f"{avg_payment:,.0f} FC",
                                icon=Icons.TRENDING_UP,
                                color=Colors.ORANGE,
                            ),
                        ],
                    ),
                    self.container_form,
                    Container(
                        content=Text(
                            self.get_text("payments_list"),
                            size=18,
                            weight=FontWeight.BOLD,
                            color=Constants.PRIMARY_COLOR,
                        ),
                        margin=Margin(top=20, bottom=10),
                    ),
                    self.search_and_pagination_container,
                    self.payments_table_container,
                ],
            )

            self._update_table()

            try:
                self.main_content.update()
            except Exception as e:
                print(f"Erreur lors de la mise à jour de l'interface: {e}")

        except Exception as e:
            print(f"Erreur lors du chargement des données: {e}")
            self.main_content.content = Text(f"Erreur: {e}")
            if hasattr(self.main_content, "update"):
                self.main_content.update()

    def build_components(self):
        self.loading_indicator = CupertinoActivityIndicator(
            animating=True, color=Constants.PRIMARY_COLOR, radius=50
        )

        self.add_button = Button(
            icon=Icons.ADD,
            tooltip=self.get_text("add_payment"),
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                bgcolor=Constants.PRIMARY_COLOR,
                padding=Padding(10, 20, 10, 20),
                color="white",
            ),
            on_click=self._open_add_form,
            content=self.get_text("add_payment"),
        )

        self.main_content = Container(
            padding=Padding.symmetric(horizontal=20, vertical=10),
            expand=True,
            content=self.loading_indicator,
            clip_behavior=ClipBehavior.ANTI_ALIAS,
            **self.get_box_style(),
        )

    def _build_add_form_components(self):
        # Student search field with suggestions
        self.student_search_field = TextField(
            label=self.get_text("search_student"),
            hint_text=self.get_text("enter_student_name"),
            on_change=self.handle_student_search_change,
            prefix_icon=Icons.SEARCH,
            suffix=IconButton(
                icon=Icons.CLEAR,
                tooltip=self.get_text("clear"),
                on_click=self.clear_student_search,
            ),
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=2,
            dense=True,
        )

        # Container pour afficher les suggestions d'élèves
        self.suggestions_container_student = Container(
            visible=False,
            width=400,
            height=250,
            bgcolor=Colors.WHITE,
            border=Border.all(1, Colors.GREY_300),
            border_radius=BorderRadius.all(5),
            padding=Padding.all(5),
        )

        # Payment type dropdown
        self.payment_type_dropdown = Dropdown(
            label=self.get_text("payment_type"),
            border_radius=BorderRadius.all(5),
            options=[],
            expand=1,
            helper_text=self.get_text("select_payment_type"),
            width=float("inf"),
            menu_width=250,
            on_change=self._on_payment_type_select,
        )

        self.amount_field_form = TextField(
            label=self.get_text("amount"),
            hint_text=self.get_text("enter_amount"),
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            expand=1,
            helper=self.get_text("amount_helper"),
            keyboard_type=KeyboardType.NUMBER,
            input_filter=NumbersOnlyInputFilter(),
        )

        self.payment_date_field = TextField(
            label=self.get_text("payment_date"),
            hint_text=self.get_text("enter_payment_date"),
            text_align=TextAlign.LEFT,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            keyboard_type=KeyboardType.DATETIME,
            value=datetime.now().strftime("%Y-%m-%d"),
            expand=1,
            helper=self.get_text("date_format_yyyy_mm_dd"),
        )

        self.student_class_text_info = Text(
            value="",
            size=14,
            color=Constants.PRIMARY_COLOR,
        )

        self.student_gender_text_info = Text(
            value="",
            size=14,
            color=Constants.PRIMARY_COLOR,
        )

        self.add_payment_submit_button = Button(
            content=self.get_text("submit"),
            icon=Icons.SAVE,
            on_click=self._submit_payment,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                bgcolor=Constants.PRIMARY_COLOR,
                padding=Padding(10, 20, 10, 20),
                color="white",
            ),
        )

        self.add_payment_cancel_button = Button(
            content=self.get_text("cancel"),
            icon=Icons.CANCEL,
            on_click=self._close_add_form,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                bgcolor=Constants.CANCEL_COLOR,
                padding=Padding(10, 20, 10, 20),
                color="white",
            ),
        )

        # Create form container
        self.container_form = Container(
            content=Column(
                horizontal_alignment=CrossAxisAlignment.STRETCH,
                controls=[
                    Text(
                        value=self.get_text("add_payment"),
                        style=TextStyle(
                            size=18,
                            weight=FontWeight.BOLD,
                            color=Constants.PRIMARY_COLOR,
                        ),
                    ),
                    Column(
                        controls=[
                            self.student_search_field,
                            self.suggestions_container_student,
                        ],
                    ),
                    Row(
                        controls=[
                            self.student_class_text_info,
                            self.student_gender_text_info,
                        ],
                        spacing=20,
                    ),
                    Row(
                        controls=[
                            self.payment_type_dropdown,
                            self.amount_field_form,
                            self.payment_date_field,
                        ],
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                    ),
                    Row(
                        controls=[
                            self.add_payment_submit_button,
                            self.add_payment_cancel_button,
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

    def _build_table_components(self):
        """Build the payments table and pagination components"""
        self.search_field = TextField(
            hint_text=self.get_text("search_by_student"),
            prefix_icon=Icons.SEARCH,
            border_color=Constants.PRIMARY_COLOR,
            focused_border_color=Constants.PRIMARY_COLOR,
            on_change=self._on_search_change,
            expand=True,
        )

        self.payment_type_filter_dropdown = Dropdown(
            label=self.get_text("filter_by_payment_type"),
            value="all",
            options=[
                DropdownOption(key="all", text=self.get_text("all_types")),
            ],
            width=250,
            on_change=self._on_payment_type_filter_change,
        )

        self.items_per_page_dropdown = Dropdown(
            label=self.get_text("items_per_page"),
            value="10",
            options=[
                DropdownOption(key="5", text="5"),
                DropdownOption(key="10", text="10"),
                DropdownOption(key="20", text="20"),
                DropdownOption(key="50", text="50"),
            ],
            width=150,
            on_change=self._on_items_per_page_change,
        )

        self.page_info_text = Text(
            value="",
            size=14,
            color=Constants.PRIMARY_COLOR,
        )

        self.prev_page_button = IconButton(
            icon=Icons.ARROW_BACK,
            icon_color=Constants.PRIMARY_COLOR,
            tooltip=self.get_text("previous"),
            on_click=self._go_to_prev_page,
            disabled=True,
        )

        self.next_page_button = IconButton(
            icon=Icons.ARROW_FORWARD,
            icon_color=Constants.PRIMARY_COLOR,
            tooltip=self.get_text("next"),
            on_click=self._go_to_next_page,
            disabled=True,
        )

        self.search_and_pagination_container = Container(
            content=Column(
                controls=[
                    Row(
                        controls=[
                            self.search_field,
                            self.payment_type_filter_dropdown,
                        ],
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    Row(
                        controls=[
                            self.items_per_page_dropdown,
                            Row(
                                controls=[
                                    self.prev_page_button,
                                    self.page_info_text,
                                    self.next_page_button,
                                ],
                                alignment=MainAxisAlignment.END,
                            ),
                        ],
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                    ),
                ],
                spacing=10,
            ),
            padding=Padding.symmetric(vertical=20, horizontal=10),
            **self.get_box_style(),
        )

        self.payments_table_container = Container(
            content=Column(
                controls=[],
                scroll=ScrollMode.AUTO,
            ),
            padding=Padding.all(10),
            **self.get_box_style(),
        )

    # --- Form management ---
    def _open_add_form(self, e):
        """Open the add payment form"""
        self.container_form.visible = True
        self.add_button.icon = Icons.CLOSE
        self.add_button.tooltip = self.get_text("close_form")
        self.add_button.content = self.get_text("close_form")
        self.add_button.style.bgcolor = Constants.CANCEL_COLOR
        self.add_button.on_click = self._close_add_form

        # Populate payment types dropdown
        self._populate_payment_types()

        self.add_button.update()
        self.container_form.update()

    def _close_add_form(self, e):
        """Close the add payment form"""
        self.container_form.visible = False
        self.add_button.icon = Icons.ADD
        self.add_button.style.bgcolor = Constants.PRIMARY_COLOR
        self.add_button.tooltip = self.get_text("add_payment")
        self.add_button.content = self.get_text("add_payment")
        self.add_button.on_click = self._open_add_form
        self._clear_form()
        self.add_button.update()
        self.container_form.update()

    def _clear_form(self):
        """Clear the payment form"""
        self.selected_student_id = None
        self.student_search_field.value = ""
        self.suggestions_container_student.visible = False
        self.student_class_text_info.value = ""
        self.student_gender_text_info.value = ""
        self.payment_type_dropdown.value = None
        self.amount_field_form.value = ""
        self.payment_date_field.value = datetime.now().strftime("%Y-%m-%d")

    def _populate_payment_types(self):
        """Populate payment types dropdown"""
        if self.payment_types_data:
            self.payment_type_dropdown.options = [
                DropdownOption(key=str(pt.id_payment_type), text=pt.name)
                for pt in self.payment_types_data
            ]
            if hasattr(self.payment_type_dropdown, "update"):
                self.payment_type_dropdown.update()

    def _on_payment_type_select(self, e):
        """Handle payment type selection and auto-fill amount"""
        if e.control.value:
            payment_type_id = int(e.control.value)
            for pt in self.payment_types_data:
                if pt.id_payment_type == payment_type_id:
                    self.amount_field_form.value = str(int(pt.amount_defined))
                    if hasattr(self.amount_field_form, "update"):
                        self.amount_field_form.update()
                    break

    async def _submit_payment(self, e):
        """Submit the payment form"""
        # Validate form
        if not self.selected_student_id:
            self.page.snack_bar = SnackBar(
                Text(self.get_text("please_select_student")),
                bgcolor=Constants.CANCEL_COLOR,
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        if not self.payment_type_dropdown.value:
            self.page.snack_bar = SnackBar(
                Text(self.get_text("please_select_payment_type")),
                bgcolor=Constants.CANCEL_COLOR,
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        if not self.amount_field_form.value:
            self.page.snack_bar = SnackBar(
                Text(self.get_text("please_enter_amount")),
                bgcolor=Constants.CANCEL_COLOR,
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        try:
            amount = float(self.amount_field_form.value)
            if amount <= 0:
                raise ValueError("Amount must be positive")
        except ValueError:
            self.page.snack_bar = SnackBar(
                Text(self.get_text("invalid_amount")),
                bgcolor=Constants.CANCEL_COLOR,
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        # Create payment data
        payment_data = {
            "student_id": self.selected_student_id,
            "payment_type_id": int(self.payment_type_dropdown.value),
            "amount": amount,
            "payment_date": self.payment_date_field.value,
            "school_year_id": self.app_state.current_school_year_id or 1,
            "user_id": (
                self.app_state.current_user.id_user
                if self.app_state.current_user
                else 1
            ),
        }

        # Submit payment
        try:
            success = await self.services.create_payment(payment_data)
            if success:
                print("Payment created successfully")
        except Exception as ex:
            # TODO
            print(f"Error creating payment: {ex}")

    # --- Student search handlers ---
    def handle_student_search_change(self, e):
        """Handle changes in student search field"""
        search_text = e.control.value.strip()

        # Hide suggestions if less than 2 characters
        if len(search_text) < 2:
            self.suggestions_container_student.visible = False
            if hasattr(self.suggestions_container_student, "update"):
                self.suggestions_container_student.update()
            return

        # Filter students based on search text
        suggestions = []
        if self.students_data:
            normalized_search = Utils.normalize_text(search_text.lower())

            for student in self.students_data:
                # Get student info
                first_name = student.first_name or ""
                last_name = student.last_name or ""
                surname = student.surname or ""
                full_name = f"{first_name} {last_name} {surname}".strip()

                # Normalize for comparison
                normalized_full_name = Utils.normalize_text(full_name.lower())
                normalized_first = Utils.normalize_text(first_name.lower())
                normalized_last = Utils.normalize_text(last_name.lower())
                normalized_surname = Utils.normalize_text(surname.lower())

                # Check if search text matches any part
                if (
                    normalized_search in normalized_full_name
                    or normalized_search in normalized_first
                    or normalized_search in normalized_last
                    or normalized_search in normalized_surname
                ):
                    suggestions.append(student)

        # Display suggestions
        self.display_student_suggestions(suggestions)

    def display_student_suggestions(self, suggestions: list[StudentModel]):
        """Display the list of student suggestions"""
        if not suggestions:
            self.suggestions_container_student.visible = False
            if hasattr(self.suggestions_container_student, "update"):
                self.suggestions_container_student.update()
            return

        # Create suggestion widgets
        suggestion_widgets = []
        for student in suggestions[:10]:  # Limit to 10 suggestions
            # Get classroom name for this student
            classroom_name = self._get_classroom_name(student.id_student)

            # Create full name
            full_name = (
                f"{student.first_name} {student.last_name} {student.surname}".strip()
            )

            # Create suggestion tile
            suggestion_tile = ListTile(
                title=Text(full_name, weight=FontWeight.BOLD),
                subtitle=Text(
                    f"Classe: {classroom_name} | Genre: {student.gender}",
                    size=12,
                ),
                leading=Icon(
                    Icons.PERSON,
                    color=(
                        Constants.PRIMARY_COLOR
                        if student.gender == "M"
                        else Colors.PINK
                    ),
                ),
                on_click=lambda e, s=student: self.select_student(s),
                bgcolor=Colors.TRANSPARENT,
                hover_color=Colors.BLUE_50,
            )
            suggestion_widgets.append(suggestion_tile)

        # Update suggestions container
        self.suggestions_container_student.content = ListView(
            controls=suggestion_widgets,
            auto_scroll=False,
            spacing=2,
            expand=True,
        )
        self.suggestions_container_student.visible = True
        if hasattr(self.suggestions_container_student, "update"):
            self.suggestions_container_student.update()

    def _get_classroom_name(self, student_id: int) -> str:
        """Get classroom name for a student"""
        for enrollment in self.enrollments_data:
            if enrollment.student_id == student_id:
                for classroom in self.classrooms_data:
                    if classroom.id_classroom == enrollment.classroom_id:
                        return classroom.name
        return "N/A"

    def select_student(self, student: StudentModel):
        """Select a student from suggestions"""
        self.selected_student_id = student.id_student

        # Build display text for search field
        full_name = (
            f"{student.first_name} {student.last_name} {student.surname}".strip()
        )
        classroom_name = self._get_classroom_name(student.id_student)

        display_text = f"{full_name}"
        if classroom_name != "N/A":
            display_text += f" - {classroom_name}"

        self.student_search_field.value = display_text

        # Update student info display
        self.student_class_text_info.value = f"Classe: {classroom_name}"
        self.student_gender_text_info.value = f"Genre: {student.gender}"

        # Hide suggestions
        self.suggestions_container_student.visible = False

        # Update interface
        if hasattr(self.student_search_field, "update"):
            self.student_search_field.update()
        if hasattr(self.suggestions_container_student, "update"):
            self.suggestions_container_student.update()
        if hasattr(self.student_class_text_info, "update"):
            self.student_class_text_info.update()
        if hasattr(self.student_gender_text_info, "update"):
            self.student_gender_text_info.update()

    def clear_student_search(self, e):
        """Clear student search"""
        self.selected_student_id = None
        self.student_search_field.value = ""
        self.student_class_text_info.value = ""
        self.student_gender_text_info.value = ""
        self.suggestions_container_student.visible = False

        # Update interface
        if hasattr(self.student_search_field, "update"):
            self.student_search_field.update()
        if hasattr(self.suggestions_container_student, "update"):
            self.suggestions_container_student.update()
        if hasattr(self.student_class_text_info, "update"):
            self.student_class_text_info.update()
        if hasattr(self.student_gender_text_info, "update"):
            self.student_gender_text_info.update()

    # --- Filter and pagination methods ---
    def _apply_filters(self):
        """Apply search and filters to payments data"""
        if not self.payments_data:
            self.filtered_payments = []
            return

        query = self.search_query.lower().strip()
        filtered = self.payments_data.copy()

        # Apply text search filter (search by student name)
        if query:
            filtered = [
                p
                for p in filtered
                if self._get_student_name(p.student_id).lower().find(query) != -1
            ]

        # Apply payment type filter
        if self.selected_payment_type_filter != "all":
            payment_type_id = int(self.selected_payment_type_filter)
            filtered = [p for p in filtered if p.payment_type_id == payment_type_id]

        self.filtered_payments = filtered

    def _update_payment_type_filter_options(self):
        """Update payment type filter dropdown options"""
        if not hasattr(self, "payment_type_filter_dropdown"):
            return

        options = [
            DropdownOption(key="all", text=self.get_text("all_types")),
        ]

        for pt in self.payment_types_data:
            options.append(DropdownOption(key=str(pt.id_payment_type), text=pt.name))

        self.payment_type_filter_dropdown.options = options

    def _on_search_change(self, e):
        """Handle search field change"""
        self.search_query = e.control.value
        self.current_page = 1
        self._apply_filters()
        self._update_table()

    def _on_payment_type_filter_change(self, e):
        """Handle payment type filter change"""
        self.selected_payment_type_filter = e.control.value
        self.current_page = 1
        self._apply_filters()
        self._update_table()

    def _on_items_per_page_change(self, e):
        """Handle items per page dropdown change"""
        self.items_per_page = int(e.control.value)
        self.current_page = 1
        self._update_table()

    def _go_to_prev_page(self, e):
        """Go to previous page"""
        if self.current_page > 1:
            self.current_page -= 1
            self._update_table()

    def _go_to_next_page(self, e):
        """Go to next page"""
        total_pages = self._get_total_pages()
        if self.current_page < total_pages:
            self.current_page += 1
            self._update_table()

    def _get_total_pages(self):
        """Calculate total number of pages"""
        if not self.filtered_payments:
            return 1
        return max(
            1,
            (len(self.filtered_payments) + self.items_per_page - 1)
            // self.items_per_page,
        )

    def _get_paginated_payments(self):
        """Get payments for current page"""
        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = start_idx + self.items_per_page
        return self.filtered_payments[start_idx:end_idx]

    # --- Helper methods ---
    def _get_student_name(self, student_id: int) -> str:
        """Get student full name by ID"""
        for student in self.students_data:
            if student.id_student == student_id:
                return f"{student.first_name} {student.last_name} {student.surname}".strip()
        return "N/A"

    def _get_payment_type_name(self, payment_type_id: int) -> str:
        """Get payment type name by ID"""
        for pt in self.payment_types_data:
            if pt.id_payment_type == payment_type_id:
                return pt.name
        return "N/A"

    def _get_classroom_name(self, student_id: int) -> str:
        """Get classroom name for a student"""
        for enrollment in self.enrollments_data:
            if enrollment.student_id == student_id:
                for classroom in self.classrooms_data:
                    if classroom.id_classroom == enrollment.classroom_id:
                        return classroom.name
        return "N/A"

    def _format_date(self, date_str: str) -> str:
        """Format date string to DD/MM/YYYY"""
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            return date_obj.strftime("%d/%m/%Y")
        except:
            return date_str

    # --- Table creation methods ---
    def _create_table_header(self):
        """Create the table header row"""
        return Container(
            content=Row(
                controls=[
                    Container(
                        content=Text(
                            self.get_text("student"),
                            weight=FontWeight.BOLD,
                            color="white",
                        ),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.get_text("classroom"),
                            weight=FontWeight.BOLD,
                            color="white",
                        ),
                        expand=1,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.get_text("payment_type"),
                            weight=FontWeight.BOLD,
                            color="white",
                        ),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.get_text("amount"),
                            weight=FontWeight.BOLD,
                            color="white",
                        ),
                        expand=1,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            self.get_text("payment_date"),
                            weight=FontWeight.BOLD,
                            color="white",
                        ),
                        expand=1,
                        padding=Padding.all(10),
                    ),
                ],
                alignment=MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor=Constants.PRIMARY_COLOR,
            border_radius=BorderRadius.only(top_left=10, top_right=10),
        )

    def _create_table_row(self, payment: PaymentModel, index: int):
        """Create a table row for a payment"""
        student_name = self._get_student_name(payment.student_id)
        classroom_name = self._get_classroom_name(payment.student_id)
        payment_type_name = self._get_payment_type_name(payment.payment_type_id)
        formatted_date = Utils.format_date(payment.payment_date)

        return Container(
            content=Row(
                controls=[
                    Container(
                        content=Text(student_name, size=14),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(classroom_name, size=14),
                        expand=1,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(payment_type_name, size=14),
                        expand=2,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(
                            f"{payment.amount:,.0f} FC", size=14, weight=FontWeight.BOLD
                        ),
                        expand=1,
                        padding=Padding.all(10),
                    ),
                    Container(
                        content=Text(formatted_date, size=14),
                        expand=1,
                        padding=Padding.all(10),
                    ),
                ],
                alignment=MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor="#f8faff" if index % 2 == 0 else "white",
            border=Border(
                bottom=BorderSide(1, Colors.GREY_200),
            ),
        )

    def _update_table(self):
        """Update the payments table with current data"""
        if not self.filtered_payments:
            self.payments_table_container.content = Column(
                controls=[
                    Container(
                        content=Text(
                            self.get_text("no_payments_found"),
                            size=16,
                            color=Colors.GREY_600,
                        ),
                        padding=Padding.all(20),
                        alignment=Alignment.CENTER,
                    )
                ],
            )
        else:
            paginated_payments = self._get_paginated_payments()
            table_rows = [self._create_table_header()]

            for idx, payment in enumerate(paginated_payments):
                table_rows.append(self._create_table_row(payment, idx))

            self.payments_table_container.content = Column(
                controls=table_rows,
                spacing=0,
                scroll=ScrollMode.AUTO,
            )

        # Update pagination info
        total_pages = self._get_total_pages()
        start_idx = (self.current_page - 1) * self.items_per_page + 1
        end_idx = min(
            self.current_page * self.items_per_page, len(self.filtered_payments)
        )

        self.page_info_text.value = (
            f"{self.get_text('page')} {self.current_page} / {total_pages} "
            f"({start_idx}-{end_idx} {self.get_text('of')} {len(self.filtered_payments)})"
        )
        self.prev_page_button.disabled = self.current_page <= 1
        self.next_page_button.disabled = self.current_page >= total_pages

        # Update UI
        try:
            self.payments_table_container.update()
            self.page_info_text.update()
            self.prev_page_button.update()
            self.next_page_button.update()
        except Exception as e:
            pass

    def create_stat_card(
        self, title: str, value: str, icon: str, color: str, subtitle: str = None
    ) -> Control:
        """Create a statistics card"""
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

    def build(self) -> Column:
        return Column(
            horizontal_alignment=CrossAxisAlignment.STRETCH,
            controls=[
                Container(
                    content=Row(
                        controls=[
                            Text(
                                value=self.get_text("payment_management"),
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
                                        on_click=self.refresh_payments_data,
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
