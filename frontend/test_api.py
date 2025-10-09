from src.data.api.fake_client import FakeApiClient
import asyncio


async def test_fake_api_client() -> None:
    api = FakeApiClient()
    users = await api.list_users()
    print(f"Total users: {len(users)}")
    for user in users:
        print(f"User: {user}")

    await api.close()


if __name__ == "__main__":
    asyncio.run(test_fake_api_client())
