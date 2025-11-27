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

    async def load_fees_data(self):
        return (True, await self.app_state.api_client.list_fees())

    async def get_user_role_by_user_id(self, user_id: int):
        role = await self.app_state.api_client.get_user_role(user_id)
        return role.role_name

    async def activate_school_year(self, school_year_id: int):
        await asyncio.sleep(0.5)
        return True
