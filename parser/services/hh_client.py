"""Клиент для работы с API hh.ru."""

import httpx
from typing import Any


class HhApiClient:
    """Асинхронный клиент для API hh.ru."""

    BASE_URL = "https://api.hh.ru"

    def __init__(self, access_token: str) -> None:
        self.access_token = access_token
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Получить или создать HTTP-клиент."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.BASE_URL,
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "User-Agent": "Jobify/1.0 (dev@jobify.local)",
                },
                timeout=30.0,
            )
        return self._client

    async def close(self) -> None:
        """Закрыть HTTP-клиент."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    async def get_vacancies(
        self,
        text: str | None = None,
        area: int | None = None,
        salary_from: int | None = None,
        salary_to: int | None = None,
        page: int = 0,
        per_page: int = 20,
        order_by: str | None = None,
        experience: str | None = None,
        employment: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
    ) -> dict[str, Any]:
        """
        Поиск вакансий.

        Args:
            text: Поисковый запрос
            area: ID региона
            salary_from: Минимальная зарплата
            salary_to: Максимальная зарплата
            page: Номер страницы
            per_page: Количество на странице (макс. 100)
            order_by: Сортировка
            experience: Требуемый опыт
            employment: Тип занятости
            date_from: Начало периода (ISO 8601)
            date_to: Конец периода (ISO 8601)

        Returns:
            Словарь с данными: items, found, pages, page, per_page
        """
        client = await self._get_client()

        params: dict[str, Any] = {
            "page": page,
            "per_page": min(per_page, 100),  # API ограничивает до 100
        }

        if text:
            params["text"] = text
        if area:
            params["area"] = area
        if salary_from:
            params["salary_from"] = salary_from
        if salary_to:
            params["salary_to"] = salary_to
        if order_by:
            params["order_by"] = order_by
        if experience:
            params["experience"] = experience
        if employment:
            params["employment"] = employment
        if date_from:
            params["date_from"] = date_from
        if date_to:
            params["date_to"] = date_to

        response = await client.get("/vacancies", params=params)
        response.raise_for_status()
        return response.json()

    async def get_vacancy(self, vacancy_id: str) -> dict[str, Any]:
        """
        Получить детали вакансии по ID.

        Args:
            vacancy_id: ID вакансии

        Returns:
            Словарь с данными вакансии
        """
        client = await self._get_client()
        response = await client.get(f"/vacancies/{vacancy_id}")
        response.raise_for_status()
        return response.json()

    async def get_areas(self) -> list[dict[str, Any]]:
        """
        Получить список регионов.

        Returns:
            Список регионов
        """
        client = await self._get_client()
        response = await client.get("/areas")
        response.raise_for_status()
        return response.json()

    async def get_professions(self) -> list[dict[str, Any]]:
        """
        Получить справочник профессий.

        Returns:
            Список профессий
        """
        client = await self._get_client()
        response = await client.get("/professions")
        response.raise_for_status()
        return response.json()

    async def get_industries(self) -> list[dict[str, Any]]:
        """
        Получить справочник отраслей.

        Returns:
            Список отраслей
        """
        client = await self._get_client()
        response = await client.get("/industries")
        response.raise_for_status()
        return response.json()

    async def get_currencies(self) -> list[dict[str, Any]]:
        """
        Получить курсы валют.

        Returns:
            Список валют
        """
        client = await self._get_client()
        response = await client.get("/currencies")
        response.raise_for_status()
        return response.json()

    async def get_employer(self, employer_id: str) -> dict[str, Any]:
        """
        Получить информацию о работодателе.

        Args:
            employer_id: ID работодателя

        Returns:
            Словарь с данными работодателя
        """
        client = await self._get_client()
        response = await client.get(f"/employers/{employer_id}")
        response.raise_for_status()
        return response.json()

    async def get_me(self) -> dict[str, Any]:
        """
        Получить информацию о текущем пользователе.

        Returns:
            Словарь с данными пользователя
        """
        client = await self._get_client()
        response = await client.get("/me")
        response.raise_for_status()
        return response.json()
