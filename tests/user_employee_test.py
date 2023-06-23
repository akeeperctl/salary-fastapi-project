from httpx import AsyncClient

from tests.conftest import TEST_VALUE_SAVER


async def test_get_me(ac: AsyncClient):
    response = await ac.get(
        url="employees/me",
        headers={
            "Authorization": "Bearer " + TEST_VALUE_SAVER.values.get("ACCESS_TOKEN")
        }
    )

    # pprint(response.json())

    assert response.status_code == 200, "Не узнал себя самого..."


async def test_get_me_salary(ac: AsyncClient):
    response = await ac.get(
        url="employees/me/salary",
        headers={
            "Authorization": "Bearer " + TEST_VALUE_SAVER.values.get("ACCESS_TOKEN")
        }
    )

    # pprint(TEST_VALUE_SAVER.values)

    assert response.status_code == 200, "Не получил зарплату"
