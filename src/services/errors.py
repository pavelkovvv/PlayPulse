"""Исключения прикладного слоя для перевода в HTTP-ответы в роутерах."""


class ServiceError(Exception):
    """Ошибка прикладного слоя: роутер преобразует в HTTP-ответ."""

    def __init__(self, status_code: int, detail: str):
        """
        :param status_code: HTTP-статус для ответа клиенту (как у FastAPI HTTPException).
        :param detail: Текст ошибки для поля detail ответа.
        """
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)
