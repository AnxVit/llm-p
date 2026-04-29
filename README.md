# Настройка проекта
**Если uv не установлен:**
```
pip install uv
```

**Установка зависимостей проекта:**
```
uv sync
```
или
```
make depends
```

*Активация виртуального окружения (опционально):*
```
source .venv/bin/active
```

**Конфигурация**
Создайте файл *.env* в корне проекта

Переменные:
- OPENROUTER_API_KEY - API ключ к openrouter
- APP_NAME - название приложения
- ENV - окружение

- JWT_SECRET - секретный ключ JWT
- JWT_ALG - алгоритм шифрование JWT
- ACCESS_TOKEN_EXPIRE_MINUTES - время жизни токена в минутах

- SQLITE_PATH - путь к папке SQLite

- OPENROUTER_BASE_URL - путь к OpenRouter
- OPENROUTER_MODEL - LLM модель
- OPENROUTER_SITE_URL - host приложения (отправлятся в openrouter)
- OPENROUTER_APP_NAME - название проекта (отправляется в openrouter)

**Запуск проекта:**
```
uv run uvicorn app.main:app --reload --host <host> --port <port>
```
или
```
make run
```

# Пример использования
## Регистрация
<img src="screenshots/register_1.png" width="600" />
<img src="screenshots/register_2.png" width="600" />

## Логин
<img src="screenshots/login_1.png" width="600" />
<img src="screenshots/login_2.png" width="600" />

## Авторизация через Swagger
<img src="screenshots/authorization_swagger_1.png" width="600" />
<img src="screenshots/authorization_swagger_2.png" width="600" />

## Вызов chat
<img src="screenshots/chat_1.png" width="600" />
<img src="screenshots/chat_2.png" width="600" />

## Получение истории сообщений
![История](screenshots/chat_history.png)

## Удаление истории сообщений
![История](screenshots/history_delete.png)