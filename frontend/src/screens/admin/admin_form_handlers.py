"""
Admin Form Handlers Module
Contains form submission logic for all admin entities
"""


class AdminFormHandlers:
    """Handles form submissions for admin entities"""

    def __init__(self, parent):
        """
        Initialize form handlers with reference to parent AdminScreen
        Args:
            parent: Reference to AdminScreen instance
        """
        self.parent = parent

    async def submit_user_form(self, e):
        """Submit user form"""
        # Validate fields
        if not self.parent.user_username_field.value:
            return

        if not self.parent.user_email_field.value:
            return

        if not self.parent.user_password_field.value:
            return

        if not self.parent.user_role_dropdown.value:
            return

        # Create user data
        user_data = {
            "username": self.parent.user_username_field.value,
            "email": self.parent.user_email_field.value,
            "password": self.parent.user_password_field.value,
            "role_id": int(self.parent.user_role_dropdown.value),
        }

        # TODO: Submit to service
        print(f"User data to submit: {user_data}")

        # Close form and refresh data
        self.parent._close_form(e)
        await self.parent.load_data()

    async def submit_classroom_form(self, e):
        """Submit classroom form"""
        # Validate fields
        if not self.parent.classroom_name_field.value:
            return

        if not self.parent.classroom_level_field.value:
            return

        # Create classroom data
        classroom_data = {
            "name": self.parent.classroom_name_field.value,
            "level": self.parent.classroom_level_field.value,
        }

        # TODO: Submit to service
        print(f"Classroom data to submit: {classroom_data}")

        # Close form and refresh data
        self.parent._close_form(e)
        await self.parent.load_data()

    async def submit_school_year_form(self, e):
        """Submit school year form"""
        # Validate fields
        if not self.parent.school_year_name_field.value:
            return

        # Create school year data
        school_year_data = {
            "name": self.parent.school_year_name_field.value,
            "start_date": self.parent.school_year_start_date_field.value,
            "end_date": self.parent.school_year_end_date_field.value,
            "is_active": self.parent.school_year_status_switch.value,
        }

        # TODO: Submit to service
        print(f"School year data to submit: {school_year_data}")

        # Close form and refresh data
        self.parent._close_form(e)
        await self.parent.load_data()

    async def submit_staff_form(self, e):
        """Submit staff form"""
        # Validate fields
        if not self.parent.staff_first_name_field.value:
            return

        if not self.parent.staff_last_name_field.value:
            return

        if not self.parent.staff_position_field.value:
            return

        if not self.parent.staff_salary_field.value:
            return

        # Create staff data
        staff_data = {
            "first_name": self.parent.staff_first_name_field.value,
            "last_name": self.parent.staff_last_name_field.value,
            "position": self.parent.staff_position_field.value,
            "hire_date": self.parent.staff_hire_date_field.value,
            "salary_base": float(self.parent.staff_salary_field.value),
        }

        # TODO: Submit to service
        print(f"Staff data to submit: {staff_data}")

        # Close form and refresh data
        self.parent._close_form(e)
        await self.parent.load_data()
