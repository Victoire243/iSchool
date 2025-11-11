import asyncio
from core import AppState


class StudentsServices:
    def __init__(self, app_state: AppState):
        self.app_state = app_state

    async def load_students_data(self):
        # await asyncio.sleep(2)  # Simulate network delay
        return (True, await self.app_state.api_client.list_students())

    async def load_students_per_classroom_data(self):
        # await asyncio.sleep(2)  # Simulate network delay
        return (True, await self.app_state.api_client.list_students_per_classroom())

    async def load_classrooms_data(self):
        # await asyncio.sleep(2)  # Simulate network delay
        return (True, await self.app_state.api_client.list_classrooms())

    async def load_enrollments_data(self):
        # await asyncio.sleep(2)  # Simulate network delay
        return (True, await self.app_state.api_client.list_enrollments())

    async def update_student(self, student):
        """Update a student"""
        # await asyncio.sleep(1)  # Simulate network delay
        return await self.app_state.api_client.update_student(student)

    async def import_students(self, students_list, classroom_id):
        """Import multiple students"""
        # await asyncio.sleep(1)  # Simulate network delay
        return await self.app_state.api_client.import_students(
            students_list, classroom_id
        )
