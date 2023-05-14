# **_Foodgram_**

Foodgram, «Продуктовый помощник». Онлайн-сервис и API. На этом сервисе реализованы возможности публикации своих рецептов, подписки на публикации других пользователей, добавления понравившихся рецептов в список «Избранное», скачивания сводного списка продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Локальный запуск проекта:

Клонируем репозиторий и переходим в него:

```bash
git clone https://github.com/Picnichek/foodgram-project-react.git
cd yamdb_final
```

Переходим в папку с файлом docker-compose.yaml:

```bash
cd infra
```

Шаблон наполнения .env (в текущем репозитории называется '.env.template') который должен быть расположен по пути infra/.env
переносим данные из '.env.template' в .env

```bash
cp .env.template .env
```

Поднимаем контейнеры (db-1, web-1, nginx-1):

```bash
docker compose up -d --build
```

Выполняем миграции:

```bash
docker compose exec web python manage.py makemigrations
```

```bash
docker compose exec web python manage.py migrate
```

Тестовая база данных и суперпользователь admin@admin.com(пароль:admin) присутствуют в файле fixtures.json, находящимся в корне проекта,
можно выполнить команду:

```bash
docker compose exec web python manage.py loaddata fixtures.json
```

Собираем статику:

```bash
docker-compose exec web python manage.py collectstatic --no-input
```

Создаем дамп базы данных (тестовая база присутствует в текущем репозитории):

```bash
docker-compose exec web python manage.py dumpdata > fixtures.json
```

Останавливаем контейнеры:

```bash
docker-compose down -v
```
