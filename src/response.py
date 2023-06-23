from typing import Optional, Any


class ShiftAPIResponse:
    def __init__(self, status: str, description: str | None, data: dict | Any, print_console: bool = False) -> object:

        self.status = status
        self.description = description
        self.data = data

        if print_console:
            print(self)
