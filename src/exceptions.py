from typing import Optional, Any, Dict

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder


# class ShiftAPIResponse:
#     def __init__(self, status: str, description: str | None, data: dict | Any, print_console: bool = False) -> object:
#         self.status = status
#         self.description = description
#         self.data = data
#
#         if print_console:
#             print(self)


class ShiftHTTPException(HTTPException):
    def __init__(
            self,
            sh_status: str | None,
            sh_desc: str | None,
            status_code: int,
            detail: Any,
            headers: Optional[Dict[str, str]] = None,
    ) -> None:
        super().__init__(
            status_code=status_code,
            detail={
                "status": sh_status,
                "description": sh_desc,
                "data": jsonable_encoder(detail)
            },
            headers=headers
        )
