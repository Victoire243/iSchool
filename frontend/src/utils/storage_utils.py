from flet import *  # type: ignore


class StorageUtils:
    @staticmethod
    async def save_to_local_storage(page: Page, key: str, value: str) -> None:
        await page.shared_preferences.set(key, value)

    @staticmethod
    async def get_from_local_storage(page: Page, key: str) -> str | None:
        return await page.shared_preferences.get(key)

    @staticmethod
    async def remove_from_local_storage(page: Page, key: str) -> None:
        await page.shared_preferences.remove(key)

    @staticmethod
    async def clear_local_storage(page: Page) -> None:
        await page.shared_preferences.clear()

    @staticmethod
    async def has_key_in_local_storage(page: Page, key: str) -> bool:
        return await page.shared_preferences.contains_key(key)
