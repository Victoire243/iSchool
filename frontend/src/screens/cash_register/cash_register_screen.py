"""
Cash Register Screen - Modular Version
=====================================
Version modulaire utilisant des fichiers séparés pour chaque fonctionnalité.

Modules utilisés:
- cash_register_components.py : Composants UI réutilisables
- cash_register_forms.py : Gestion des formulaires
- cash_register_form_handlers.py : Logique de soumission des formulaires
- cash_register_tables.py : Gestion des tables de données
- cash_register_dialogs.py : Gestion des dialogues
- cash_register_services.py : Services de données
"""

from flet import *  # type: ignore
import asyncio
from datetime import datetime
from core import AppState, Constants
from .cash_register_services import CashRegisterServices
from .cash_register_components import CashRegisterComponents
from .cash_register_forms import CashRegisterForms
from .cash_register_form_handlers import CashRegisterFormHandlers
from .cash_register_tables import CashRegisterTables
from .cash_register_dialogs import CashRegisterDialogs


class CashRegisterScreen:
    """
    Écran de gestion de la caisse (Version modulaire).
    Délègue les fonctionnalités spécifiques à des modules dédiés.
    """

    def __init__(self, app_state: AppState, page: Page):
        self.app_state = app_state
        self.page = page
        self.services = CashRegisterServices(app_state)

        # Initialize data structures
        self.entries_data = []
        self.statistics = {}
        self.staff_data = []
        self.current_filter = "all"  # all, income, expense

        # Initialize modules
        self.forms = CashRegisterForms(self)
        self.form_handlers = CashRegisterFormHandlers(self)
        self.tables = CashRegisterTables(self)
        self.dialogs = CashRegisterDialogs(self)

        # Build UI components
        self.build_components()
        self._build_table_components()
        self.dialogs.build_all_dialogs()

    # ========================================================================
    # LIFECYCLE METHODS
    # ========================================================================

    async def on_mount(self):
        """Called when the screen is mounted"""
        await self.load_data()

    def refresh_data(self, e):
        """Refresh all cash register data"""
        self.main_content.content = self.loading_indicator
        self.main_content.update()
        asyncio.create_task(self.load_data())

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def get_text(self, key: str) -> str:
        """Get translated text for a given key"""
        return self.app_state.translations.get(key, key)

    @staticmethod
    def get_box_style() -> dict:
        """Return common box styling"""
        return CashRegisterComponents.get_box_style()

    # ========================================================================
    # DATA LOADING
    # ========================================================================

    async def load_data(self):
        """Load all necessary data for the cash register screen"""
        try:
            # Load data in parallel
            (
                (entries_status, entries_data),
                (stats_status, statistics),
                (staff_status, staff_data),
            ) = await asyncio.gather(
                self.services.load_cash_register_entries(),
                self.services.get_statistics(),
                self.services.load_staff_list(),
                return_exceptions=True,
            )

            # Store data
            self.entries_data = entries_data if entries_status else []
            self.statistics = statistics if stats_status else {}
            self.staff_data = staff_data if staff_status else []

            # Populate staff dropdown
            self.forms.populate_staff_dropdown(self.staff_data)

            # Calculate statistics for display
            total_income = self.statistics.get("total_income", 0.0)
            total_expenses = self.statistics.get("total_expenses", 0.0)
            balance = self.statistics.get("balance", 0.0)

            # Update main content with stats and table
            self.main_content.content = Column(
                expand=True,
                horizontal_alignment=CrossAxisAlignment.STRETCH,
                scroll=ScrollMode.AUTO,
                controls=[
                    # Statistics cards
                    Row(
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        spacing=20,
                        controls=[
                            CashRegisterComponents.create_stat_card(
                                title=self.get_text("total_balance"),
                                value=CashRegisterComponents.format_currency(balance),
                                icon=Icons.ACCOUNT_BALANCE_WALLET,
                                color=Colors.BLUE if balance >= 0 else Colors.RED,
                                subtitle=self.get_text("current_balance"),
                            ),
                            CashRegisterComponents.create_stat_card(
                                title=self.get_text("total_income"),
                                value=CashRegisterComponents.format_currency(total_income),
                                icon=Icons.TRENDING_UP,
                                color=Colors.GREEN,
                                subtitle=f"{int(self.statistics.get('income_count', 0))} {self.get_text('entries')}",
                            ),
                            CashRegisterComponents.create_stat_card(
                                title=self.get_text("total_expenses"),
                                value=CashRegisterComponents.format_currency(total_expenses),
                                icon=Icons.TRENDING_DOWN,
                                color=Colors.RED,
                                subtitle=f"{int(self.statistics.get('expense_count', 0))} {self.get_text('entries')}",
                            ),
                        ],
                    ),
                    # Filter and action buttons
                    Container(
                        content=Row(
                            [
                                self._build_filter_buttons(),
                                Row(
                                    [
                                        self.quick_entry_button,
                                        self.staff_payment_button,
                                    ],
                                    spacing=10,
                                ),
                            ],
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        margin=Margin(top=20, bottom=10),
                    ),
                    # Forms container
                    self.forms_container,
                    # Data table
                    self.data_table_container,
                ],
            )

            # Update table with current filter
            await self._apply_filter()

            try:
                self.main_content.update()
            except Exception as e:
                print(f"Erreur lors de la mise à jour de l'interface: {e}")
        except Exception as e:
            print(f"Erreur lors du chargement des données: {e}")
            self.main_content.content = Text(f"Erreur: {e}")
            if hasattr(self.main_content, "update"):
                self.main_content.update()

    # ========================================================================
    # MAIN UI COMPONENTS
    # ========================================================================

    def build_components(self):
        """Build main UI components"""
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

        # Forms container (initially hidden)
        self.forms_container = Container(
            padding=Padding.all(15),
            margin=Margin(top=10, bottom=10),
            expand=False,
            visible=False,
            clip_behavior=ClipBehavior.ANTI_ALIAS,
            **self.get_box_style(),
        )

        # Quick entry button
        self.quick_entry_button = ElevatedButton(
            text=self.get_text("quick_entry"),
            icon=Icons.ADD,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                bgcolor=Constants.PRIMARY_COLOR,
                padding=Padding(10, 20, 10, 20),
                color="white",
            ),
            on_click=self._open_quick_entry_form,
        )

        # Staff payment button
        self.staff_payment_button = ElevatedButton(
            text=self.get_text("staff_payment"),
            icon=Icons.PERSON,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                bgcolor=Constants.SECONDARY_COLOR,
                padding=Padding(10, 20, 10, 20),
                color="white",
            ),
            on_click=self._open_staff_payment_form,
        )

    def _build_filter_buttons(self):
        """Build filter buttons for entry types"""
        return Row(
            controls=[
                TextButton(
                    text=self.get_text("all_entries"),
                    style=ButtonStyle(
                        bgcolor=Constants.PRIMARY_COLOR
                        if self.current_filter == "all"
                        else Colors.TRANSPARENT,
                        color="white"
                        if self.current_filter == "all"
                        else Constants.PRIMARY_COLOR,
                        padding=Padding.symmetric(horizontal=20, vertical=10),
                    ),
                    on_click=lambda e: asyncio.create_task(
                        self._set_filter("all")
                    ),
                ),
                TextButton(
                    text=self.get_text("income"),
                    style=ButtonStyle(
                        bgcolor=Colors.GREEN
                        if self.current_filter == "income"
                        else Colors.TRANSPARENT,
                        color="white"
                        if self.current_filter == "income"
                        else Colors.GREEN,
                        padding=Padding.symmetric(horizontal=20, vertical=10),
                    ),
                    on_click=lambda e: asyncio.create_task(
                        self._set_filter("income")
                    ),
                ),
                TextButton(
                    text=self.get_text("expense"),
                    style=ButtonStyle(
                        bgcolor=Colors.RED
                        if self.current_filter == "expense"
                        else Colors.TRANSPARENT,
                        color="white"
                        if self.current_filter == "expense"
                        else Colors.RED,
                        padding=Padding.symmetric(horizontal=20, vertical=10),
                    ),
                    on_click=lambda e: asyncio.create_task(
                        self._set_filter("expense")
                    ),
                ),
            ],
            spacing=10,
        )

    def _build_table_components(self):
        """Build table container"""
        self.data_table_container = Container(
            content=Column(
                controls=[],
                scroll=ScrollMode.AUTO,
            ),
            padding=Padding.all(10),
            **self.get_box_style(),
        )

    # ========================================================================
    # FORM MANAGEMENT
    # ========================================================================

    def _open_quick_entry_form(self, e):
        """Open quick entry form"""
        self.forms_container.content = self.forms.quick_entry_form_container
        self.forms_container.visible = True

        # Update buttons
        self.quick_entry_button.style.bgcolor = Constants.CANCEL_COLOR
        self.quick_entry_button.icon = Icons.CLOSE
        self.quick_entry_button.on_click = self._close_form

        self.forms_container.update()
        self.quick_entry_button.update()

    def _open_staff_payment_form(self, e):
        """Open staff payment form"""
        self.forms_container.content = self.forms.staff_payment_form_container
        self.forms_container.visible = True

        # Update buttons
        self.staff_payment_button.style.bgcolor = Constants.CANCEL_COLOR
        self.staff_payment_button.icon = Icons.CLOSE
        self.staff_payment_button.on_click = self._close_form

        self.forms_container.update()
        self.staff_payment_button.update()

    def _close_form(self, e):
        """Close the form"""
        self.forms_container.visible = False

        # Reset buttons
        self.quick_entry_button.icon = Icons.ADD
        self.quick_entry_button.style.bgcolor = Constants.PRIMARY_COLOR
        self.quick_entry_button.on_click = self._open_quick_entry_form

        self.staff_payment_button.icon = Icons.PERSON
        self.staff_payment_button.style.bgcolor = Constants.SECONDARY_COLOR
        self.staff_payment_button.on_click = self._open_staff_payment_form

        self.forms.clear_all_forms()

        self.forms_container.update()
        self.quick_entry_button.update()
        self.staff_payment_button.update()

    # ========================================================================
    # FILTER MANAGEMENT
    # ========================================================================

    async def _set_filter(self, filter_type: str):
        """Set the current filter and update table"""
        self.current_filter = filter_type
        await self._apply_filter()

        # Rebuild filter buttons to reflect new state
        try:
            self.main_content.update()
        except:
            pass

    async def _apply_filter(self):
        """Apply current filter to entries"""
        if self.current_filter == "all":
            filtered_entries = self.entries_data
        elif self.current_filter == "income":
            filtered_entries = [e for e in self.entries_data if e.type == "Entrée"]
        else:  # expense
            filtered_entries = [e for e in self.entries_data if e.type == "Sortie"]

        await self.tables.update_entries_table(filtered_entries)

    # ========================================================================
    # DIALOG MANAGEMENT
    # ========================================================================

    def _open_entry_edit_dialog(self, entry):
        """Open entry edit dialog"""
        self.dialogs.open_entry_edit_dialog(entry)

    def _open_entry_delete_dialog(self, entry):
        """Open entry delete dialog"""
        self.dialogs.open_entry_delete_dialog(entry)

    # ========================================================================
    # RECEIPT PRINTING
    # ========================================================================

    def _print_receipt(self, entry):
        """Generate and display receipt for an entry"""
        receipt_text = f"""
══════════════════════════════════════
           {self.get_text("receipt")}
══════════════════════════════════════

{self.get_text("date")}: {CashRegisterComponents.format_date(entry.date)}
{self.get_text("type")}: {entry.type}
{self.get_text("description")}:
{entry.description}

{self.get_text("amount")}: {CashRegisterComponents.format_currency(entry.amount)}

══════════════════════════════════════
        {self.get_text("thank_you")}
══════════════════════════════════════
        """

        # Create receipt dialog
        receipt_dialog = AlertDialog(
            title=Text(self.get_text("receipt"), weight=FontWeight.BOLD),
            content=Container(
                content=Text(
                    receipt_text,
                    size=14,
                    font_family="Courier New",
                ),
                width=400,
            ),
            actions=[
                TextButton(
                    text=self.get_text("close"),
                    on_click=lambda e: self._close_receipt_dialog(receipt_dialog),
                ),
            ],
        )

        self.page.overlay.append(receipt_dialog)
        receipt_dialog.open = True
        self.page.update()

    def _close_receipt_dialog(self, dialog):
        """Close receipt dialog"""
        dialog.open = False
        self.page.update()

    # ========================================================================
    # MAIN BUILD METHOD
    # ========================================================================

    def build(self) -> Column:
        """Build the main cash register screen layout"""
        return Column(
            horizontal_alignment=CrossAxisAlignment.STRETCH,
            controls=[
                Container(
                    content=Row(
                        controls=[
                            Text(
                                value=self.get_text("cash_register"),
                                size=24,
                                weight=FontWeight.BOLD,
                                color=Constants.PRIMARY_COLOR,
                            ),
                            IconButton(
                                icon=Icons.REFRESH,
                                icon_color=Constants.PRIMARY_COLOR,
                                tooltip=self.get_text("refresh"),
                                on_click=self.refresh_data,
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
