from pprint import pprint

from httpx import AsyncClient
from tests.conftest import TEST_VALUE_SAVER


async def test_get_me(ac: AsyncClient):
    response = await ac.get(
        url="employees/me",
        headers={
            "Authorization": "Bearer " + TEST_VALUE_SAVER.values.get("ACCESS_TOKEN")
        }
    )

    assert response.status_code == 200, "Не узнал себя самого..."


async def test_patch_me(ac: AsyncClient):
    response = await ac.patch(
        url="employees/me",
        headers={
            "Authorization": "Bearer " + TEST_VALUE_SAVER.values.get("ACCESS_TOKEN")
        },
        json={
            "email": "alien@keeper.com",
            "password": "verystrong",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "job_id": TEST_VALUE_SAVER.values.get("CREATED_JOB").get("id"),
            "username": "hahahah",
            "firstname": "vsvsvsvs",
            "lastname": "vdvdvdv"
        }
    )

    assert response.status_code == 200, "Не изменил себя"


async def test_get_me_salary(ac: AsyncClient):
    response = await ac.get(
        url="employees/me/salary",
        headers={
            "Authorization": "Bearer " + TEST_VALUE_SAVER.values.get("ACCESS_TOKEN")
        }
    )

    assert response.status_code == 200, "Не получил зарплату"
    pprint(response.json())
