from httpx import AsyncClient
from starlette import status

from tests.conftest import TEST_VALUE_SAVER


# Перед началом теста нужно установить зн. True
# в фикстуре is_super_user в файле conftest.py


async def test_get_user(ac: AsyncClient):
    response = await ac.get(
        url="employees/1",
        headers={
            "Authorization": "Bearer " + TEST_VALUE_SAVER.values.get("ACCESS_TOKEN")
        }
    )

    assert response.status_code == status.HTTP_200_OK, "Не получил пользователя"


async def test_patch_user(ac: AsyncClient):
    response = await ac.patch(
        url="employees/1",
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

    assert response.status_code == status.HTTP_200_OK, "Не изменил пользователя"


async def test_delete_user(ac: AsyncClient):
    response = await ac.delete(
        url="employees/1",
        headers={
            "Authorization": "Bearer " + TEST_VALUE_SAVER.values.get("ACCESS_TOKEN")
        }
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT, "Не удалил пользователя"


async def test_add_job(ac: AsyncClient):
    response = await ac.post(
        url="jobs/add",
        headers={
            "Authorization": "Bearer " + TEST_VALUE_SAVER.values.get("ACCESS_TOKEN")
        },
        json={
            "salary": 25000,
            "title": "уборщик",
            "description": "моет пол"
        }
    )

    assert response.status_code == status.HTTP_201_CREATED, "Не создал рабочее место"


async def test_get_job(ac: AsyncClient):
    response = await ac.get(
        url="jobs/2",
        headers={
            "Authorization": "Bearer " + TEST_VALUE_SAVER.values.get("ACCESS_TOKEN")
        },
    )

    assert response.status_code == status.HTTP_200_OK, "Не получил рабочее место"


async def test_patch_job(ac: AsyncClient):
    response = await ac.patch(
        url="jobs/2",
        headers={
            "Authorization": "Bearer " + TEST_VALUE_SAVER.values.get("ACCESS_TOKEN")
        },
        json={
            "salary": 15000,
            "title": "string",
            "description": "string"
        }
    )

    assert response.status_code == status.HTTP_200_OK, "Не изменил рабочее место"


async def test_get_all_jobs(ac: AsyncClient):
    response = await ac.get(
        url="jobs/all/",
        headers={
            "Authorization": "Bearer " + TEST_VALUE_SAVER.values.get("ACCESS_TOKEN")
        },
        params={
            "limit": 15,
            "offset": 0
        }
    )

    assert response.status_code == status.HTTP_200_OK, "Не получил список работы"
