"""Тестовый скрипт для проверки HH API клиента."""

import asyncio
import os
import sys

# Добавляем проект в путь
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jobify.settings")

from parser.services.hh_client import HhApiClient


async def main() -> None:
    """Тестирование клиента."""
    # Токен из .env
    token = "APPLMU0CKQVBP7SA08PF4FPD10E03BTV3CTS0J9L0M0L4CKLDTSS608VUG3R1K41"

    client = HhApiClient(access_token=token)

    try:
        # Тест: поиск вакансий Python разработчика
        print("🔍 Поиск вакансий: Python разработчик, Москва...")
        result = await client.get_vacancies(
            text="Python разработчик",
            area=1,  # Москва
            per_page=5,
        )

        print(f"\n📊 Найдено вакансий: {result.get('found', 0)}")
        print(f"📄 Страниц: {result.get('pages', 0)}")
        print(f"📍 Текущая страница: {result.get('page', 0)}")

        print("\n" + "=" * 60)
        for i, vacancy in enumerate(result.get("items", [])[:3], 1):
            print(f"\n{i}. {vacancy.get('name', 'N/A')}")
            print(f"   Работодатель: {vacancy.get('employer', {}).get('name', 'N/A')}")

            salary = vacancy.get("salary")
            if salary:
                from_val = salary.get("from")
                to_val = salary.get("to")
                currency = salary.get("currency")
                if from_val or to_val:
                    print(f"   Зарплата: {from_val or ''} {'-' if from_val and to_val else ''} {to_val or ''} {currency or ''}")

            print(f"   Город: {vacancy.get('area', {}).get('name', 'N/A')}")
            print(f"   Ссылка: {vacancy.get('alternate_url', 'N/A')}")

        print("\n✅ Тест успешно завершён!")

    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        raise

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
