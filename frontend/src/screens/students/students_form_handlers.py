from flet import *
from core import Constants
from models import StudentModel
import asyncio


class StudentsFormHandlers:
    def __init__(self, students_screen):
        self.screen = students_screen

    def clear_form(self):
        self.screen.full_name_field_form.value = ""
        self.screen.birth_date_field_form.value = "01-01-2000"
        if self.screen.classroom_form.options:
            self.screen.classroom_form.value = self.screen.classroom_form.options[0].key
        self.screen.gender_form.value = None
        self.screen.address_field_form.value = ""
        self.screen.parent_contact_field_form.value = ""
        self.screen.full_name_field_form.update()
        self.screen.birth_date_field_form.update()
        self.screen.classroom_form.update()
        self.screen.gender_form.update()
        self.screen.address_field_form.update()
        self.screen.parent_contact_field_form.update()

    def open_add_form(self, e):
        self.screen.container_form.visible = True
        self.screen.add_button.icon = Icons.CLOSE
        self.screen.add_button.tooltip = self.screen.get_text("close_form")
        self.screen.add_button.content = self.screen.get_text("close_form")
        self.screen.add_button.style.bgcolor = Constants.CANCEL_COLOR
        self.screen.add_button.on_click = self.close_add_form
        self.screen.add_button.update()
        self.screen.container_form.update()

    def close_add_form(self, e):
        self.screen.container_form.visible = False
        self.screen.add_button.icon = Icons.ADD
        self.screen.add_button.style.bgcolor = Constants.PRIMARY_COLOR
        self.screen.add_button.tooltip = self.screen.get_text("add_student")
        self.screen.add_button.content = self.screen.get_text("add_student")
        self.screen.add_button.on_click = self.open_add_form
        self.clear_form()
        self.screen.add_button.update()
        self.screen.container_form.update()

    async def submit_add_form(self, e):
        def extraite_names():
            try:
                names = self.screen.full_name_field_form.value.strip().split(" ")
                if len(names) >= 3:
                    return names[0], names[1], " ".join(names[2:])
                elif len(names) == 2:
                    return names[0], names[1], ""
                elif len(names) == 1:
                    return names[0], "", ""
                else:
                    return "", "", ""
            except:
                return "", "", ""

        if (
            not self.screen.full_name_field_form.value.strip()
            or not self.screen.birth_date_field_form.value.strip()
            or not self.screen.classroom_form.value
            or not self.screen.gender_form.value
        ):
            return
        first_name, last_name, surname = extraite_names()
        birth_date = self.screen.birth_date_field_form.value.strip()
        classroom_id = int(self.screen.classroom_form.value)
        gender = self.screen.gender_form.value
        adress = self.screen.address_field_form.value.strip()
        parent_contact = self.screen.parent_contact_field_form.value.strip()

        print(
            f"Adding new student: {first_name} {last_name} {surname}, DOB: {birth_date}, Classroom ID: {classroom_id}, Gender: {gender}, Address: {adress}, Parent Contact: {parent_contact}"
        )
        response = await self.screen.services.create_student(
            StudentModel.from_dict(
                {
                    "first_name": first_name,
                    "last_name": last_name,
                    "surname": surname,
                    "gender": gender,
                    "date_of_birth": birth_date,
                    "address": adress,
                    "parent_contact": parent_contact,
                    "is_deleted": False,
                }
            )
        )
        if response:
            print("Student created successfully")
            # Refresh data after successful creation
            await self.screen.load_data()
            self.close_add_form(None)
        else:
            print("Error while creating student")

    async def save_student_changes(self, e):
        """Save changes to the student"""
        try:
            # Get updated values
            updated_student = StudentModel(
                id_student=self.screen.current_editing_student_id,
                first_name=self.screen.edit_first_name_field.value.strip(),
                last_name=self.screen.edit_last_name_field.value.strip(),
                surname=self.screen.edit_surname_field.value.strip(),
                gender=self.screen.edit_gender_dropdown.value,
                date_of_birth=self.screen.edit_birth_date_field.value.strip(),
                address=self.screen.edit_address_field.value.strip(),
                parent_contact=self.screen.edit_parent_contact_field.value.strip(),
            )

            # TODO: Call API to update student
            # success = await self.screen.services.update_student(updated_student)

            # For now, update locally
            for i, student in enumerate(self.screen.students_data):
                if student.id_student == self.screen.current_editing_student_id:
                    self.screen.students_data[i] = updated_student
                    break

            # Update enrollment if classroom changed
            selected_classroom_id = int(self.screen.edit_classroom_dropdown.value)
            for enrollment in self.screen.enrollments_data:
                if enrollment.student_id == self.screen.current_editing_student_id:
                    enrollment.classroom_id = selected_classroom_id
                    break

            # Close dialog
            self.screen.dialogs.close_edit_dialog()

            # Refresh the table
            self.screen.tables.apply_filters()
            self.screen.tables.update_table()

        except Exception as ex:
            print(f"Error updating student: {ex}")
            self.screen.page.show_snack_bar(
                SnackBar(
                    content=Text(self.screen.get_text("error_updating_student")),
                    bgcolor=Colors.RED,
                )
            )

    async def confirm_delete_student(self, e):
        """Confirm deletion of the student"""
        # TODO implementation here
        self.screen.dialogs.close_delete_dialog()
