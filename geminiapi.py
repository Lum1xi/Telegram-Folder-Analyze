import aiohttp
import asyncio
from config import GEMINI_KEY

API_KEY = GEMINI_KEY
MODEL_NAME = "gemini-2.5-flash"

# URL для Gemini API
# Зверніть увагу, що ключ API додається як параметр запиту
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"


async def call_gemini_api(session, payload):
    """Асинхронна функція для надсилання POST-запиту до Gemini API."""

    headers = {
        "Content-Type": "application/json"
    }

    print("Відправка запиту до API...")

    try:
        # Використовуємо session.post для асинхронного запиту
        async with session.post(URL, json=payload, headers=headers) as response:

            # Перевіряємо статус відповіді
            if response.status == 200:
                # Асинхронно читаємо відповідь як JSON
                data = await response.json()

                # Обробляємо та виводимо текстову відповідь
                try:
                    text_response = data['candidates'][0]['content']['parts'][0]['text']
                    return text_response
                except KeyError:
                    return f"Помилка: Не вдалося розпарсити відповідь. {data}"
            else:
                # Асинхронно читаємо текст помилки
                error_text = await response.text()
                return f"Помилка API: {response.status} - {error_text}"

    except aiohttp.ClientConnectorError as e:
        return f"Помилка з'єднання: {e}"
    except Exception as e:
        return f"Виникла неочікувана помилка: {e}"


async def generate_text(prompt: str, request_text) -> str:
    """High-level helper: sends a simple text prompt to Gemini and returns the text response."""
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt + "\n" + request_text}
                ]
            }
        ]
    }
    async with aiohttp.ClientSession() as session:
        return await call_gemini_api(session, payload)


async def main():
    """Головна асинхронна функція."""

    # Дані (payload), які ми надсилаємо.
    # Це простий текстовий запит.
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "Привіт, світе! Розкажи мені короткий факт про космос."
                    }
                ]
            }
        ]
    }

    # Створюємо асинхронну сесію
    async with aiohttp.ClientSession() as session:
        # Викликаємо нашу функцію API
        response_text = await call_gemini_api(session, payload)

        print("\n--- Відповідь від Gemini ---")
        print(response_text)
        print("----------------------------")


# Запускаємо головну асинхронну функцію
if __name__ == "__main__":
    asyncio.run(main())