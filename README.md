# **_Foodgram_**

![CI](https://github.com/picnichek/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

## Описание проекта
http://158.160.47.115/ - внешний ip<br>
foodgram-delicious.ddns.net - доменное имя<br>
http://158.160.47.115/api/docs/ - редок можно глянуть тут<br>
Сервер оставляю включенным.<br>
Foodgram, «Продуктовый помощник». Онлайн-сервис и API. На этом сервисе реализованы возможности публикации своих рецептов, подписки на публикации других пользователей, добавления понравившихся рецептов в список «Избранное», скачивания сводного списка продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Локальный запуск проекта

**Клонируем репозиторий и переходим в него:**

```bash
git clone https://github.com/Picnichek/foodgram-project-react.git
cd yamdb_final
```

**Переходим в папку с файлом docker-compose.yaml:**

```bash
cd infra
```

**Шаблон наполнения .env** (в текущем репозитории называется '.env.template') который должен быть расположен по пути infra/.env
переносим данные из '.env.template' в .env:

```bash
cp .env.template .env
```

**Поднимаем контейнеры** (db-1, web-1, nginx-1):

```bash
docker compose up -d --build
```

**Выполняем миграции:**

```bash
docker compose exec web python manage.py makemigrations
```

```bash
docker compose exec web python manage.py migrate
```

В файле fixtures.json, находящимся в корне проекта, присутствуют следующие данные:
- Тестовая база данных;
- суперпользователь admin@admin.com (пароль:admin);
    - тестовые пользователи: 
        - vpupkin@yandex.ru (пароль: Qwerty1234!); 
        - example@example.com (пароль: example).<br>

Для добавления их в **БД** нужно выполнить команду:

```bash
docker compose exec web python manage.py loaddata fixtures.json
```

**Собираем статику:**

```bash
docker compose exec web python manage.py collectstatic --no-input
```

**При необходимости можно создать дамп базы данных** (тестовая база присутствует в текущем репозитории):

```bash
docker compose exec web python manage.py dumpdata > fixtures.json
```

**При завершении работы останавливаем контейнеры**:

```bash
docker compose down -v
```

## Запуск проекта на удаленном сервере

**Клонируем репозиторий и переходим в него:**

```bash
git clone https://github.com/Picnichek/foodgram-project-react.git
cd yamdb_final
```

**Заходим в settings.py и указываем свой внешний ip и доменное имя в ALLOWED_HOSTS**

```bash
ALLOWED_HOSTS = [
    'web',
    'ip', 
    'site_name.com',
    'localhost',
    '127.0.0.1',
    '[::1]',
    'testserver',
]
```

**Установливаем на сервере Docker, Docker Compose:**

```bash
sudo apt install curl                                   - установка утилиты для скачивания файлов
curl -fsSL https://get.docker.com -o get-docker.sh      - скачать скрипт для установки
sh get-docker.sh                                        - запуск скрипта
sudo apt-get install docker-compose-plugin              - последняя версия docker compose
```

**Скопировать на сервер файлы docker-compose.yml, nginx.conf из папки infra (команды выполнять находясь в папке infra):**

```bash
scp docker-compose.yml nginx.conf username@IP:/home/username/

# username - имя пользователя на сервере
# IP - публичный IP сервера
```

**В файле nginx.conf необходимо указать свой адрес сервера и доменное имя в строке "server_name"**

```bash
server_name ip host_name.com;
```

**Для работы с GitHub Actions необходимо в репозитории в разделе Secrets - Actions создать переменные окружения:**

```bash
DOCKER_PASSWORD         - пароль от Docker Hub
DOCKER_USERNAME         - логин Docker Hub
HOST                    - публичный IP сервера
USER                    - имя пользователя на сервере
PASSPHRASE              - *если ssh-ключ защищен паролем
SSH_KEY                 - приватный ssh-ключ, узнать можно с помощью "cat ~/.ssh/id_rsa" по умолчанию
TELEGRAM_TO             - ID телеграм-аккаунта для посылки сообщения
TELEGRAM_TOKEN          - токен бота, посылающего сообщение

DB_NAME                 - postgres
POSTGRES_USER           - postgres
POSTGRES_PASSWORD       - postgres
DB_HOST                 - db
DB_PORT                 - 5432 (порт по умолчанию)
```

**Выполнить шаги описанные с шага "Поднимаем контейнеры" из инструкции "Локальный запуск проекта"**


**После каждого обновления репозитория (push в ветку master) будет происходить:**

1. Проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8)
2. Сборка и доставка докер-образов frontend и backend на Docker Hub
3. Разворачивание проекта на удаленном сервере
4. Отправка сообщения в Telegram в случае успеха
