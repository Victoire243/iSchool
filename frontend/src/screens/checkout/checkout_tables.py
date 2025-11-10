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
        # Pagination state
        self.current_page = 1
        self.items_per_page = 10

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

            # Get paginated entries
            paginated_entries = self._get_paginated_transactions(filtered_entries)

            # Build transaction items
            if not paginated_entries:
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
                    for entry in paginated_entries
                ]

            # Update pagination controls
            self._update_pagination_controls(len(filtered_entries))

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
            on_change=lambda e: self._on_filter_change(e),
            width=200,
        )

        # Pagination controls
        self.screen.items_per_page_dropdown = Dropdown(
            label=self.screen.get_text("items_per_page"),
            value="10",
            options=[
                dropdown.Option("5", "5"),
                dropdown.Option("10", "10"),
                dropdown.Option("20", "20"),
                dropdown.Option("50", "50"),
            ],
            width=150,
            on_change=lambda e: self._on_items_per_page_change(e),
        )

        self.screen.page_info_text = Text(
            value="",
            size=14,
            color=Constants.PRIMARY_COLOR,
        )

        self.screen.prev_page_button = IconButton(
            icon=Icons.ARROW_BACK,
            icon_color=Constants.PRIMARY_COLOR,
            tooltip=self.screen.get_text("previous"),
            on_click=lambda e: self._go_to_prev_page(e),
            disabled=True,
        )

        self.screen.next_page_button = IconButton(
            icon=Icons.ARROW_FORWARD,
            icon_color=Constants.PRIMARY_COLOR,
            tooltip=self.screen.get_text("next"),
            on_click=lambda e: self._go_to_next_page(e),
            disabled=True,
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
                    Row(
                        controls=[
                            self.screen.items_per_page_dropdown,
                            Row(
                                controls=[
                                    self.screen.prev_page_button,
                                    self.screen.page_info_text,
                                    self.screen.next_page_button,
                                ],
                                alignment=MainAxisAlignment.END,
                            ),
                        ],
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                    ),
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

    # ========================================================================
    # PAGINATION METHODS
    # ========================================================================

    def _get_paginated_transactions(self, filtered_entries):
        """Get transactions for current page"""
        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = start_idx + self.items_per_page
        return filtered_entries[start_idx:end_idx]

    def _get_total_pages(self, total_items):
        """Calculate total number of pages"""
        if total_items == 0:
            return 1
        return max(1, (total_items + self.items_per_page - 1) // self.items_per_page)

    def _update_pagination_controls(self, total_items):
        """Update pagination controls state"""
        total_pages = self._get_total_pages(total_items)

        # Update page info text
        if hasattr(self.screen, "page_info_text"):
            self.screen.page_info_text.value = (
                f"{self.screen.get_text('page')} {self.current_page} "
                f"{self.screen.get_text('of')} {total_pages}"
            )

        # Update button states
        if hasattr(self.screen, "prev_page_button"):
            self.screen.prev_page_button.disabled = self.current_page <= 1

        if hasattr(self.screen, "next_page_button"):
            self.screen.next_page_button.disabled = self.current_page >= total_pages

        # Update controls if they have a page
        if hasattr(self.screen, "page_info_text") and self.screen.page_info_text.page:
            try:
                self.screen.page_info_text.update()
            except Exception:
                pass

        if (
            hasattr(self.screen, "prev_page_button")
            and self.screen.prev_page_button.page
        ):
            try:
                self.screen.prev_page_button.update()
            except Exception:
                pass

        if (
            hasattr(self.screen, "next_page_button")
            and self.screen.next_page_button.page
        ):
            try:
                self.screen.next_page_button.update()
            except Exception:
                pass

    def _on_filter_change(self, e):
        """Handle filter dropdown change"""
        self.current_page = 1
        self.screen.page.run_task(self.update_transactions_table)

    def _on_items_per_page_change(self, e):
        """Handle items per page dropdown change"""
        self.items_per_page = int(e.control.value)
        self.current_page = 1
        self.screen.page.run_task(self.update_transactions_table)

    def _go_to_prev_page(self, e):
        """Go to previous page"""
        if self.current_page > 1:
            self.current_page -= 1
            self.screen.page.run_task(self.update_transactions_table)

    def _go_to_next_page(self, e):
        """Go to next page"""
        # Get current filter to calculate total pages correctly
        current_filter = (
            self.screen.transaction_filter.value
            if hasattr(self.screen, "transaction_filter")
            else "all"
        )

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

        total_pages = self._get_total_pages(len(filtered_entries))
        if self.current_page < total_pages:
            self.current_page += 1
            self.screen.page.run_task(self.update_transactions_table)
