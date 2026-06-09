# Poker Academy Bot

Telegram-бот для обучения покеру: теория, тренажёр, виды покера, партнёрские ссылки.

## Стек

- Python 3.11+
- [aiogram 3.x](https://docs.aiogram.dev/)
- SQLite (aiosqlite)

## Локальный запуск

```bash
pip install -r requirements.txt
cp .env.example .env
# Укажите BOT_TOKEN и ADMIN_IDS в .env
python main.py
```

## Деплой на [Bothost](https://bothost.ru)

1. Создайте репозиторий на GitHub и загрузите код
2. Зарегистрируйтесь на [bothost.ru](https://bothost.ru)
3. Создайте бота: **Telegram → Aiogram 3**
4. Укажите URL репозитория и ветку `main`
5. Добавьте переменные окружения:

| Переменная | Значение |
|------------|----------|
| `BOT_TOKEN` | Токен от @BotFather |
| `ADMIN_IDS` | Ваш Telegram user ID |
| `DB_PATH` | `/app/data/poker_academy.db` |

6. Для webhook (рекомендуется на Bothost): включите **«Использовать домен»** — платформа задаст `DOMAIN`, бот автоматически переключится на webhook

7. Для polling: `WEBHOOK_MODE=polling`

## Структура проекта

```
poker-academy-bot/
├── main.py              # Точка входа
├── requirements.txt
├── database.py
├── config/
│   ├── config.py
│   └── affiliates.py
├── handlers/
├── keyboards/
├── localization/
├── states/
└── utils/
```

## Команды бота

- `/start` — регистрация и выбор языка
- `/admin` — статистика (только для ADMIN_IDS)

## Безопасность

- Не коммитьте `.env` с токеном в Git
- Если токен утёк — перевыпустите его в @BotFather
