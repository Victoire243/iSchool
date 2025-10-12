import asyncio
from core import AppState


class DashboardServices:
    def __init__(self, app_state: AppState):
        self.app_state = app_state

    async def load_dashboard_summary(self) -> tuple[bool, dict]:
        # await asyncio.sleep(2)  # Simulate network delay
        return (True, await self.app_state.api_client.get_dashboard_summary())
