import asyncio
from core import AppState


class CheckoutServices:

    def __init__(self, app_state: AppState):
        self.app_state = app_state

    async def list_cash_register_entries(self):
        return (True, await self.app_state.api_client.list_cash_register_entries())
