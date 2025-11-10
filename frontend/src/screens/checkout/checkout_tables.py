"""
Checkout Tables Module
Contains table builders and handlers for the checkout screen
"""

from flet import *  # type: ignore
from core import Constants
from .checkout_components import CheckoutComponents


class CheckoutTables:
    """Table builders for checkout operations"""

    def __init__(self, checkout_screen):
        self.screen = checkout_screen

    async def update_transactions_table(self):
        """Update the transactions table with current data"""
        try:
            # Get current filter
            current_filter = (
                self.screen.transaction_filter.value
                if hasattr(self.screen, "transaction_filter")
                else "all"
            )

            # Filter entries based on selection
            filtered_entries = []
            if current_filter == "all":
                filtered_entries = self.screen.cash_entries_data
            elif current_filter == "entry":
                filtered_entries = [
                    e for e in self.screen.cash_entries_data if e.type == "Entrée"
                ]
            elif current_filter == "exit":
                filtered_entries = [
                    e for e in self.screen.cash_entries_data if e.type == "Sortie"
                ]

            # Build transaction items
            if not filtered_entries:
                self.screen.transactions_list.controls = [
                    CheckoutComponents.create_empty_state(
                        self.screen.get_text("no_transactions_found"),
                        Icons.RECEIPT_LONG,
                    )
                ]
            else:
                self.screen.transactions_list.controls = [
                    CheckoutComponents.create_transaction_item(
                        date=entry.date,
                        description=entry.description,
                        amount=entry.amount,
                        transaction_type=entry.type,
                        on_click=lambda e, entry=entry: self.screen.show_transaction_details(
                            entry
                        ),
                    )
                    for entry in filtered_entries[:20]  # Limit to 20 most recent
                ]

            # Only update if the control has a page (is added to the page)
            if self.screen.transactions_list.page:
                try:
                    self.screen.transactions_list.update()
                except Exception as e:
                    print(f"Error updating transactions list: {e}")

        except Exception as e:
            print(f"Error updating transactions table: {e}")

    def build_transactions_list_view(self) -> Container:
        """Build the transactions list view"""
        self.screen.transaction_filter = Dropdown(
            label=self.screen.get_text("filter_transactions"),
            border_color=Constants.PRIMARY_COLOR,
            options=[
                dropdown.Option("all", self.screen.get_text("all_transactions")),
                dropdown.Option("entry", self.screen.get_text("entries_only")),
                dropdown.Option("exit", self.screen.get_text("exits_only")),
            ],
            value="all",
            on_change=lambda e: self.screen.page.run_task(
                self.update_transactions_table
            ),
            width=200,
        )

        self.screen.transactions_list = Column(
            controls=[
                CheckoutComponents.create_empty_state(
                    self.screen.get_text("loading"), Icons.HOURGLASS_EMPTY
                )
            ],
            scroll=ScrollMode.AUTO,
            expand=True,
        )

        return Container(
            content=Column(
                controls=[
                    Row(
                        controls=[
                            CheckoutComponents.create_section_header(
                                self.screen.get_text("recent_transactions"),
                                Icons.RECEIPT_LONG,
                            ),
                            self.screen.transaction_filter,
                        ],
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                    ),
                    Divider(height=1, color=Colors.GREY_300),
                    self.screen.transactions_list,
                ],
                spacing=15,
                expand=True,
            ),
            padding=Padding.all(20),
            expand=True,
            **CheckoutComponents.get_box_style(),
        )

    def build_statistics_cards(self) -> Row:
        """Build statistics cards row"""
        return Row(
            controls=[
                CheckoutComponents.create_stat_card(
                    title=self.screen.get_text("total_entries"),
                    value="$ 0",
                    icon=Icons.ARROW_DOWNWARD,
                    color=Colors.GREEN,
                    subtitle=self.screen.get_text("student_payments"),
                ),
                CheckoutComponents.create_stat_card(
                    title=self.screen.get_text("total_exits"),
                    value="$ 0",
                    icon=Icons.ARROW_UPWARD,
                    color=Colors.RED,
                    subtitle=self.screen.get_text("expenses_and_salaries"),
                ),
                CheckoutComponents.create_stat_card(
                    title=self.screen.get_text("current_balance"),
                    value="$ 0",
                    icon=Icons.ACCOUNT_BALANCE_WALLET,
                    color=Constants.PRIMARY_COLOR,
                    subtitle=self.screen.get_text("available_cash"),
                ),
            ],
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            spacing=20,
        )

    def update_statistics_cards(self, stats: dict):
        """Update statistics cards with new data"""
        try:
            if hasattr(self.screen, "statistics_row") and self.screen.statistics_row:
                # Update the values in the existing cards
                cards = self.screen.statistics_row.controls
                if len(cards) >= 3:
                    # Update total entries card
                    cards[0].content.controls[1].controls[
                        1
                    ].value = f"$ {stats['total_in']:,.0f}"

                    # Update total exits card
                    cards[1].content.controls[1].controls[
                        1
                    ].value = f"$ {stats['total_out']:,.0f}"

                    # Update balance card
                    cards[2].content.controls[1].controls[
                        1
                    ].value = f"$ {stats['balance']:,.0f}"

                    # Only update if the control has a page (is added to the page)
                    if self.screen.statistics_row.page:
                        try:
                            self.screen.statistics_row.update()
                        except Exception as e:
                            print(f"Error updating statistics row: {e}")
        except Exception as e:
            print(f"Error updating statistics cards: {e}")
