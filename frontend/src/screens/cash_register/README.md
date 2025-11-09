# Cash Register Module

## Overview

The Cash Register (Caisse) module is a comprehensive financial management system for tracking all monetary transactions in the school. It provides real-time balance tracking, transaction management, and financial reporting capabilities.

## Architecture

The module follows a modular architecture with clear separation of concerns:

```
cash_register/
├── cash_register_screen.py       # Main screen orchestration
├── cash_register_services.py     # Data fetching & business logic
├── cash_register_components.py   # Reusable UI components
├── cash_register_forms.py        # Form definitions
├── cash_register_form_handlers.py # Form submission logic
├── cash_register_tables.py       # Data table management
└── cash_register_dialogs.py      # Edit/delete dialogs
```

## Features

### 1. Statistics Dashboard
- **Total Balance**: Shows current cash balance (color-coded: blue if positive, red if negative)
- **Total Income**: Displays total income with entry count
- **Total Expenses**: Shows total expenses with entry count

### 2. Transaction Management
- **Quick Entry Form**: Rapid data entry for expenses and income
  - Entry type selection (Income/Expense)
  - Date picker
  - Description field
  - Amount input with validation
  
### 3. Staff Payment System
- Dedicated form for processing staff payments
- Staff member selection dropdown
- Automatic entry creation as "Sortie" (expense)
- Payment date and amount tracking

### 4. Advanced Filtering
- Filter by entry type:
  - All Entries
  - Income only (Entrée)
  - Expense only (Sortie)
- Visual feedback on active filter
- Real-time table updates

### 5. Data Table
- Comprehensive display with columns:
  - ID
  - Type (with color-coded badges)
  - Date (formatted as DD/MM/YYYY)
  - Description
  - Amount (formatted with currency)
- Action buttons per row:
  - Edit
  - Delete
  - Print Receipt

### 6. Edit & Delete Operations
- Modal dialogs for editing entries
- Confirmation dialogs for deletion
- Data validation
- User feedback via snackbars

### 7. Receipt System
- Professional receipt formatting
- Transaction details display
- Print-ready layout
- Modal presentation

### 8. Export Functionality
- CSV export for filtered entries
- Preview before export
- Entry count display
- Formatted data output

## Usage

### Adding a Quick Entry

1. Click the "Saisie Rapide" button
2. Select entry type (Entrée/Sortie)
3. Fill in:
   - Date (defaults to today)
   - Description
   - Amount
4. Click "Soumettre"

### Processing Staff Payment

1. Click "Paiement du Personnel" button
2. Select staff member from dropdown
3. Enter payment date and amount
4. Click "Effectuer le paiement"

### Filtering Entries

1. Click on filter buttons:
   - "Toutes les entrées" - Show all
   - "Entrée" - Show income only
   - "Sortie" - Show expenses only
2. Table updates automatically

### Editing an Entry

1. Click the edit icon (pencil) on any row
2. Modify fields in the dialog
3. Click "Enregistrer" to save changes

### Deleting an Entry

1. Click the delete icon (trash) on any row
2. Confirm deletion in the dialog
3. Entry is permanently removed

### Exporting Data

1. Apply desired filters
2. Click "Exporter" button
3. Review preview in dialog
4. Copy CSV content for use in Excel/Sheets

## API Methods

The module uses the following API methods from `fake_client.py`:

- `list_cash_register_entries()` - Get all entries
- `filter_cash_register_entries(start_date, end_date, entry_type)` - Filter entries
- `get_cash_register_statistics()` - Get statistics
- `create_cash_register_entry(...)` - Create new entry
- `update_cash_register_entry(...)` - Update existing entry
- `delete_cash_register_entry(id_cash)` - Delete entry

## Data Model

### CashRegisterModel

```python
{
    "id_cash": int,          # Primary key
    "school_year_id": int,   # Foreign key to SchoolYearModel
    "date": str,             # Date in YYYY-MM-DD format
    "type": str,             # "Entrée" or "Sortie"
    "description": str,      # Transaction description
    "amount": float,         # Transaction amount
    "user_id": int           # Foreign key to UserModel
}
```

## Translation Keys

The module uses the following translation keys (available in French and English):

### Screen Labels
- `cash_register` - Page title
- `total_balance` - Balance card title
- `total_income` - Income card title
- `total_expenses` - Expenses card title
- `quick_entry` - Quick entry button
- `staff_payment` - Staff payment button
- `export` - Export button

### Form Labels
- `entry_type` - Entry type field
- `income` - Income option
- `expense` - Expense option
- `date` - Date field
- `description` - Description field
- `amount` - Amount field
- `select_staff` - Staff dropdown
- `payment_date` - Payment date field

### Actions
- `submit` - Submit button
- `save` - Save button
- `clear` - Clear button
- `edit` - Edit action
- `delete` - Delete action
- `print_receipt` - Print receipt action

### Messages
- `entry_created_success` - Success message
- `entry_creation_failed` - Error message
- `description_required` - Validation message
- `amount_required` - Validation message
- `invalid_amount` - Validation message

## Validation Rules

### Quick Entry Form
- Description: Required, non-empty
- Amount: Required, must be a positive number
- Date: Required, valid date format (YYYY-MM-DD)
- Entry Type: Required, must be "Entrée" or "Sortie"

### Staff Payment Form
- Staff: Required, must select a staff member
- Amount: Required, must be a positive number
- Date: Required, valid date format

## Error Handling

The module implements comprehensive error handling:

- API call failures are caught and logged
- User-friendly error messages via snackbars
- Form validation prevents invalid submissions
- Graceful degradation on data loading errors

## Performance Considerations

- Async operations for non-blocking UI
- Parallel data loading using `asyncio.gather()`
- Efficient filtering without re-fetching data
- Local state management to minimize API calls

## Future Enhancements

See the main PR description for a comprehensive list of proposed enhancements including:

- Visual charts and analytics
- Advanced date filtering with calendar picker
- Category management
- Recurring transactions
- Bulk operations
- Smart alerts and notifications
- Audit trail
- Multi-currency support

## Development Notes

### Adding a New Entry Type

To add a new entry type (e.g., "Transfer"):

1. Update the dropdown options in `cash_register_forms.py`
2. Add color mapping in `cash_register_components.py:create_entry_type_badge()`
3. Update filtering logic in `cash_register_screen.py:_apply_filter()`
4. Add translation keys to language files

### Adding a New Statistic Card

To add a new statistic:

1. Update `get_cash_register_statistics()` in `fake_client.py`
2. Add stat card in `cash_register_screen.py:load_data()`
3. Use `CashRegisterComponents.create_stat_card()` for consistent styling

### Adding a New Action to Table

To add a new action button:

1. Add IconButton in `cash_register_tables.py:update_entries_table()`
2. Create handler method in `cash_register_screen.py`
3. Add translation key if needed

## Testing

To test the module:

1. Verify all CRUD operations work correctly
2. Test filtering with different entry types
3. Validate form submissions with various inputs
4. Check error handling with invalid data
5. Test export functionality
6. Verify receipt generation
7. Check statistics calculations
8. Test UI responsiveness

## Dependencies

- `flet` - UI framework
- `asyncio` - Async operations
- `datetime` - Date handling
- `csv` - Export functionality
- `core.AppState` - Application state
- `core.Constants` - Application constants

## License

Part of the iSchool application.

## Contributors

- Initial implementation: Copilot + Victoire243
