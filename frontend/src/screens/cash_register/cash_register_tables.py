"""
Cash Register Tables Module
Handles table display and management for cash register entries
"""

from flet import *  # type: ignore
from .cash_register_components import CashRegisterComponents


class CashRegisterTables:
    """Handles table creation and updates for cash register screen"""

    def __init__(self, screen):
        self.screen = screen

    async def update_entries_table(self, entries=None):
        """Update cash register entries table"""
        if entries is None:
            entries = self.screen.entries_data

        # Create data table rows
        rows = []
        for entry in entries:
            rows.append(
                DataRow(
                    cells=[
                        DataCell(
                            Text(entry.id_cash, size=12)
                        ),
                        DataCell(
                            CashRegisterComponents.create_entry_type_badge(entry.type)
                        ),
                        DataCell(
                            Text(
                                CashRegisterComponents.format_date(entry.date),
                                size=12,
                            )
                        ),
                        DataCell(
                            Text(
                                entry.description,
                                size=12,
                                max_lines=2,
                                overflow=TextOverflow.ELLIPSIS,
                            )
                        ),
                        DataCell(
                            Text(
                                CashRegisterComponents.format_currency(entry.amount),
                                size=12,
                                weight=FontWeight.BOLD,
                                color=Colors.GREEN if entry.type == "Entrée" else Colors.RED,
                            )
                        ),
                        DataCell(
                            Row(
                                controls=[
                                    IconButton(
                                        icon=Icons.EDIT,
                                        icon_color=Colors.BLUE,
                                        icon_size=20,
                                        tooltip=self.screen.get_text("edit"),
                                        on_click=lambda e, entry=entry: self.screen._open_entry_edit_dialog(
                                            entry
                                        ),
                                    ),
                                    IconButton(
                                        icon=Icons.DELETE,
                                        icon_color=Colors.RED,
                                        icon_size=20,
                                        tooltip=self.screen.get_text("delete"),
                                        on_click=lambda e, entry=entry: self.screen._open_entry_delete_dialog(
                                            entry
                                        ),
                                    ),
                                    IconButton(
                                        icon=Icons.PRINT,
                                        icon_color=Colors.ORANGE,
                                        icon_size=20,
                                        tooltip=self.screen.get_text("print_receipt"),
                                        on_click=lambda e, entry=entry: self.screen._print_receipt(
                                            entry
                                        ),
                                    ),
                                ],
                                spacing=0,
                            )
                        ),
                    ],
                )
            )

        # Create the data table
        data_table = DataTable(
            columns=[
                DataColumn(Text(self.screen.get_text("id"), weight=FontWeight.BOLD)),
                DataColumn(Text(self.screen.get_text("type"), weight=FontWeight.BOLD)),
                DataColumn(Text(self.screen.get_text("date"), weight=FontWeight.BOLD)),
                DataColumn(
                    Text(self.screen.get_text("description"), weight=FontWeight.BOLD)
                ),
                DataColumn(
                    Text(self.screen.get_text("amount"), weight=FontWeight.BOLD)
                ),
                DataColumn(
                    Text(self.screen.get_text("actions"), weight=FontWeight.BOLD)
                ),
            ],
            rows=rows,
            border=Border.all(width=1, color=Colors.GREY_300),
            border_radius=BorderRadius.all(10),
            vertical_lines=BorderSide(width=1, color=Colors.GREY_200),
            horizontal_lines=BorderSide(width=1, color=Colors.GREY_200),
            heading_row_color=Colors.GREY_100,
            heading_row_height=50,
            data_row_min_height=60,
            data_row_max_height=80,
            show_checkbox_column=False,
        )

        # Update the table container
        self.screen.data_table_container.content = Column(
            controls=[
                data_table if rows else Text(
                    self.screen.get_text("no_entries_found"),
                    size=16,
                    color=Colors.GREY_600,
                    text_align=TextAlign.CENTER,
                )
            ],
            scroll=ScrollMode.AUTO,
            expand=True,
        )

        try:
            self.screen.data_table_container.update()
        except Exception as e:
            print(f"Error updating table: {e}")
