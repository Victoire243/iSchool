"""
Checkout Screen - Modular Version
==================================
Page de gestion de la caisse avec architecture modulaire.

Modules utilisés:
- checkout_services.py : Gestion des appels API et logique métier
- checkout_components.py : Composants UI réutilisables
- checkout_forms.py : Gestion des formulaires
- checkout_form_handlers.py : Logique de soumission des formulaires
- checkout_tables.py : Gestion des tables et listes
- checkout_dialogs.py : Gestion des dialogues
"""

from flet import *  # type: ignore
from core import AppState, Constants
import asyncio

from .checkout_services import CheckoutServices
from .checkout_components import CheckoutComponents
from .checkout_forms import CheckoutForms
from .checkout_form_handlers import CheckoutFormHandlers
from .checkout_tables import CheckoutTables
from .checkout_dialogs import CheckoutDialogs


class CheckoutScreen:
    """
    Écran de gestion de la caisse (Version modulaire).
    Gère les entrées/sorties, statistiques, dépenses rapides et paie du personnel.
    """

    def __init__(self, appState: AppState, page: Page | None = None) -> None:
        self.app_state = appState
        self.page = page
        self.services = CheckoutServices(self.app_state)

        # Initialize data structures
        self.cash_entries_data = []
        self.expenses_data = []
        self.staff_payments_data = []
        self.staff_list = []
        self.statistics = {"total_in": 0.0, "total_out": 0.0, "balance": 0.0}

        # Selection state
        self.selected_staff_id = None

        # Initialize modules
        self.forms = CheckoutForms(self)
        self.form_handlers = CheckoutFormHandlers(self)
        self.tables = CheckoutTables(self)
        self.dialogs = CheckoutDialogs(self)

        # Build UI components
        self.build_components()

    # ========================================================================
    # LIFECYCLE METHODS
    # ========================================================================

    async def on_mount(self):
        """Called when the screen is mounted"""
        await self.load_data()

    def refresh_checkout_data(self, e):
        """Refresh all checkout data"""
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
        return CheckoutComponents.get_box_style()

    # ========================================================================
    # DATA LOADING
    # ========================================================================

    async def load_data(self):
        """Load all necessary data for the checkout screen"""
        try:
            # Load data in parallel
            (
                (cash_status, cash_data),
                (expenses_status, expenses_data),
                (staff_payments_status, staff_payments_data),
                (staff_status, staff_data),
                (stats_status, stats_data),
            ) = await asyncio.gather(
                self.services.load_cash_register_entries(),
                self.services.load_expenses(),
                self.services.load_staff_payments(),
                self.services.load_staff_list(),
                self.services.get_cash_statistics(),
                return_exceptions=True,
            )

            # Store data
            self.cash_entries_data = cash_data if cash_status else []
            self.expenses_data = expenses_data if expenses_status else []
            self.staff_payments_data = (
                staff_payments_data if staff_payments_status else []
            )
            self.staff_list = staff_data if staff_status else []
            self.statistics = stats_data if stats_status else self.statistics

            # Update main content
            self.update_main_content()

            # Update statistics cards
            self.tables.update_statistics_cards(self.statistics)

            # Update transactions table
            await self.tables.update_transactions_table()

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
    # UI UPDATE METHODS
    # ========================================================================

    def update_main_content(self):
        """Update main content with all sections"""
        # Build statistics cards
        self.statistics_row = self.tables.build_statistics_cards()

        # Build action buttons
        action_buttons = Row(
            controls=[
                CheckoutComponents.create_action_button(
                    text=self.get_text("quick_entry"),
                    icon=Icons.ADD_CIRCLE,
                    color=Colors.GREEN,
                    on_click=self.toggle_quick_entry_form,
                    tooltip=self.get_text("add_quick_entry_tooltip"),
                ),
                CheckoutComponents.create_action_button(
                    text=self.get_text("quick_expense"),
                    icon=Icons.REMOVE_CIRCLE,
                    color=Colors.ORANGE,
                    on_click=self.toggle_quick_expense_form,
                    tooltip=self.get_text("add_quick_expense_tooltip"),
                ),
                CheckoutComponents.create_action_button(
                    text=self.get_text("staff_payment"),
                    icon=Icons.PAYMENTS,
                    color=Constants.PRIMARY_COLOR,
                    on_click=self.toggle_staff_payment_form,
                    tooltip=self.get_text("pay_staff_tooltip"),
                ),
            ],
            alignment=MainAxisAlignment.START,
            spacing=15,
        )

        # Build form containers
        self.quick_entry_form_container = Container(
            content=self.forms.build_quick_entry_form(),
            padding=Padding.all(20),
            visible=False,
            **self.get_box_style(),
        )

        self.quick_expense_form_container = Container(
            content=self.forms.build_quick_expense_form(),
            padding=Padding.all(20),
            visible=False,
            **self.get_box_style(),
        )

        self.staff_payment_form_container = Container(
            content=self.forms.build_staff_payment_form(),
            padding=Padding.all(20),
            visible=False,
            **self.get_box_style(),
        )

        # Build transactions list
        transactions_view = self.tables.build_transactions_list_view()

        # Update main content
        self.main_content.content = Column(
            expand=True,
            horizontal_alignment=CrossAxisAlignment.STRETCH,
            scroll=ScrollMode.AUTO,
            controls=[
                self.statistics_row,
                Container(height=20),
                Container(
                    content=action_buttons,
                    padding=Padding.all(20),
                    **self.get_box_style(),
                ),
                Container(height=10),
                self.quick_entry_form_container,
                self.quick_expense_form_container,
                self.staff_payment_form_container,
                Container(height=10),
                transactions_view,
            ],
        )

    # ========================================================================
    # FORM TOGGLE METHODS
    # ========================================================================

    def toggle_quick_entry_form(self, e):
        """Toggle quick entry form visibility"""
        self.quick_entry_form_container.visible = (
            not self.quick_entry_form_container.visible
        )
        # Hide other forms
        self.quick_expense_form_container.visible = False
        self.staff_payment_form_container.visible = False
        try:
            self.main_content.update()
        except Exception:
            pass

    def toggle_quick_expense_form(self, e):
        """Toggle quick expense form visibility"""
        self.quick_expense_form_container.visible = (
            not self.quick_expense_form_container.visible
        )
        # Hide other forms
        self.quick_entry_form_container.visible = False
        self.staff_payment_form_container.visible = False
        try:
            self.main_content.update()
        except Exception:
            pass

    def toggle_staff_payment_form(self, e):
        """Toggle staff payment form visibility"""
        self.staff_payment_form_container.visible = (
            not self.staff_payment_form_container.visible
        )
        # Hide other forms
        self.quick_entry_form_container.visible = False
        self.quick_expense_form_container.visible = False

        try:
            self.main_content.update()
        except Exception:
            pass

    # ========================================================================
    # DIALOG METHODS
    # ========================================================================

    def show_transaction_details(self, entry):
        """Show transaction details dialog"""
        # print(entry)
        dialog = self.dialogs.build_transaction_details_dialog(entry)
        self.page.show_dialog(dialog=dialog)

    def print_receipt(self, entry):
        """Show receipt preview dialog"""
        self.close_dialog()
        dialog = self.dialogs.build_receipt_dialog(entry)
        self.page.show_dialog(dialog=dialog)

    def show_success_dialog(self, message: str):
        """Show success dialog"""
        dialog = self.dialogs.build_success_dialog(message)
        self.page.show_dialog(dialog=dialog)

    def show_error_dialog(self, message: str):
        """Show error dialog"""
        dialog = self.dialogs.build_error_dialog(message)
        self.page.show_dialog(dialog=dialog)

    def close_dialog(self):
        """Close current dialog"""
        try:
            self.page.pop_dialog()
        except Exception:
            pass

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

    def build(self) -> Column:
        """Build the main checkout screen layout"""
        return Column(
            horizontal_alignment=CrossAxisAlignment.STRETCH,
            controls=[
                Container(
                    content=Row(
                        controls=[
                            Text(
                                value=self.get_text("checkout_management"),
                                size=24,
                                weight=FontWeight.BOLD,
                                color=Constants.PRIMARY_COLOR,
                            ),
                            IconButton(
                                icon=Icons.REFRESH,
                                icon_color=Constants.PRIMARY_COLOR,
                                tooltip=self.get_text("refresh"),
                                on_click=self.refresh_checkout_data,
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
