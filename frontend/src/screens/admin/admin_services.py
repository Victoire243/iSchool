import asyncio
from core import AppState


class AdminServices:
    def __init__(self, app_state: AppState):
        self.app_state = app_state

    async def load_users_data(self):
        return (True, await self.app_state.api_client.list_users())

    async def load_classrooms_data(self):
        return (True, await self.app_state.api_client.list_classrooms())

    async def load_staff_data(self):
        return (True, await self.app_state.api_client.list_staff())

    async def load_school_years_data(self):
        return (True, await self.app_state.api_client.list_school_years())
