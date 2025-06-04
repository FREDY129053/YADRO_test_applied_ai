# Тестовое задание "URL Shorter"

Сервис API(без UI), который позволяет из исходной ссылки получить короткую(за исключением домена длина 9 символов).

## Установка и запуск
```bash
git clone https://github.com/FREDY129053/YADRO_test_applied_ai.git
cd YADRO_test_applied_ai
```

1) 🐳 запустите Docker
2) 📄 создайте файл .env: 
    - 🐧 Linux/MacOS: ```cp app/src/config/.env.example app/src/config/.env```;
    - ⚡ Windows(cmd): ```copy app\src\config\.env.example app\src\config\.env```;
3) ▶️ выполните команду в консоли в репозитории: ```make all```
4) ⏳ ожидайте окончания запуска

5) 📘 Документация API будет доступна по адресу:
👉 http://localhost:8080/docs

📝 P.S. Docker используется для запуска БД. Вы можете использовать локальную PostgreSQL, просто измените параметры подключения в .env. (Схема всё равно создаётся при запуске приложения)

## Стэк технологий
1) ⚡ Fast API 
2) 🐘 СУБД PostgreSQL
3) 🐢 Tortoise ORM

## 🔄 Дополнение
- ✅ Выполнены все опциональные требования

- 🕒 Проверка актуальности ссылок:

  - При каждом переходе по ссылке

  - Плюс 🔁 через фоновый скрипт Apscheduler, который каждые 15 секунд проверяет базу на актуальность

## Конфигурация .env
```ini
DOMEN=http://localhost:8080
EXPIRE_MINUTES=2  # Время актуальности ссылки в минутах

# Настройки БД
DB_PORT=5433
DB_HOST=localhost
DB_NAME=url_shorter_db
DB_USERNAME=postgres
DB_PASSWORD=12345
```