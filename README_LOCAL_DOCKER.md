# CarWager - Руководство по запуску

## О проекте
CarWager - платформа для продажи автомобилей и проведения аукционов. Проект построен на Django с использованием PostgreSQL, Redis, WebSockets (Django Channels) и Docker.

## Содержание
1. [Локальный запуск (без Docker)](#локальный-запуск-без-docker)
2. [Запуск с Docker](#запуск-с-docker)
3. [Запуск с Docker Compose](#запуск-с-docker-compose)
4. [Настройка окружения](#настройка-окружения)
5. [Администрирование](#администрирование)
6. [Устранение неполадок](#устранение-неполадок)

---

## Локальный запуск (без Docker)

### Предварительные требования
- Python 3.8+
- PostgreSQL 12+
- Redis 6+
- Virtualenv (рекомендуется)

### 1. Установка системных зависимостей

#### Ubuntu/Debian:
```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Python и инструментов
sudo apt install -y python3.8 python3.8-venv python3.8-dev python3-pip

# Установка PostgreSQL
sudo apt install -y postgresql postgresql-contrib postgresql-server-dev-12
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Установка Redis
sudo apt install -y redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Установка системных библиотек
sudo apt install -y libpq-dev build-essential
```

#### macOS:
```bash
# Установка Homebrew (если не установлен)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Установка зависимостей
brew install python@3.8 postgresql@12 redis
brew services start postgresql@12
brew services start redis
```

### 2. Настройка базы данных PostgreSQL

```bash
# Переключение на пользователя postgres
sudo -u postgres psql

# В интерфейсе PostgreSQL выполнить:
CREATE DATABASE carwager;
CREATE USER carwager WITH PASSWORD 'carwager';
ALTER ROLE carwager SET client_encoding TO 'utf8';
ALTER ROLE carwager SET default_transaction_isolation TO 'read committed';
ALTER ROLE carwager SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE carwager TO carwager;
\q
```

### 3. Настройка проекта

```bash
# Клонирование репозитория (если еще не клонирован)
git clone <repository-url>
cd carwager

# Создание виртуального окружения
python3.8 -m venv venv
source venv/bin/activate  # Для Windows: venv\Scripts\activate

# Установка зависимостей Python
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Создайте файл `.env` в корне проекта:
```bash
# База данных
POSTGRES_NAME=carwager
POSTGRES_USER=carwager
POSTGRES_PASS=carwager
POSTGRES_HOST=localhost

# Redis
REDIS_HOST=localhost

# Django
DEBUG=True
SECRET_KEY=ваш-секретный-ключ-здесь

# Дополнительные настройки
ALLOWED_HOSTS=localhost,127.0.0.1
```

Для генерации SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Настройка Django

```bash
# Применение миграций
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Сбор статических файлов
python manage.py collectstatic --noinput

# Создание кэш-таблиц для Django RQ
python manage.py create_cache_table
```

### 6. Запуск сервисов

#### В первом терминале - Django сервер:
```bash
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

#### Во втором терминале - Redis (если не запущен):
```bash
redis-server
```

#### В третьем терминале - Django RQ worker:
```bash
source venv/bin/activate
python manage.py rqworker default
```

#### В четвертом терминале - Daphne (для WebSockets):
```bash
source venv/bin/activate
daphne -b 0.0.0.0 -p 8001 general.asgi:application
```

### 7. Проверка работоспособности

Откройте в браузере:
- Основное приложение: http://localhost:8000
- Админ-панель: http://localhost:8000/admin
- WebSocket endpoint: ws://localhost:8001/ws/

---

## Запуск с Docker

### Предварительные требования
- Docker 20.10+
- Docker Compose 2.0+

### 1. Сборка и запуск

```bash
# Клонирование репозитория
git clone <repository-url>
cd carwager

# Создание .env файла (см. раздел выше)
cp .env.example .env  # или создайте вручную

# Сборка образов
docker-compose build

# Запуск контейнеров
docker-compose up -d

# Просмотр логов
docker-compose logs -f
```

### 2. Настройка базы данных в Docker

```bash
# Приме��ение миграций
docker-compose exec django python manage.py migrate

# Создание суперпользователя
docker-compose exec django python manage.py createsuperuser

# Сбор статических файлов
docker-compose exec django python manage.py collectstatic --noinput

# Создание кэш-таблиц
docker-compose exec django python manage.py create_cache_table
```

### 3. Проверка работоспособности

После запуска откройте в браузере:
- Основное приложение: http://localhost:8080
- Админ-панель: http://localhost:8080/admin

### 4. Управление контейнерами

```bash
# Остановка контейнеров
docker-compose down

# Перезапуск контейнеров
docker-compose restart

# Просмотр запущенных контейнеров
docker-compose ps

# Просмотр логов конкретного сервиса
docker-compose logs django
docker-compose logs postgres
docker-compose logs redis
```

---

## Запуск с Docker Compose

### Файл docker-compose.yml

Проект уже содержит настроенный `docker-compose.yml` со следующими сервисами:

1. **django** - Основное Django приложение
2. **postgres** - База данных PostgreSQL
3. **redis** - Кэш и брокер сообщений
4. **nginx** - Веб-сервер и прокси
5. **daphne** - ASGI сервер для WebSockets
6. **worker** - Фоновые задачи Django RQ

### Команды для работы

```bash
# Полный запуск всех сервисов
docker-compose up -d

# Запуск только базы данных и Redis
docker-compose up -d postgres redis

# Запуск Django с зависимостями
docker-compose up -d django

# Остановка всех сервисов
docker-compose down

# Остановка с удалением volumes
docker-compose down -v

# Пересборка конкретного сервиса
docker-compose build django
docker-compose up -d django

# Выполнение команд в контейнере
docker-compose exec django python manage.py shell
docker-compose exec postgres psql -U carwager -d carwager
```

### Мониторинг

```bash
# Просмотр использования ресурсов
docker stats

# Просмотр логов в реальном времени
docker-compose logs -f --tail=50

# Проверка здоровья сервисов
docker-compose ps
```

---

## Настройка окружения

### Файл .env

Основные переменные окружения:

```env
# Django
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# База данных
POSTGRES_NAME=carwager
POSTGRES_USER=carwager
POSTGRES_PASS=carwager
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Docker специфичные
DOCKER_ENV=true
COMPOSE_PROJECT_NAME=carwager
```

### Настройка для продакшена

Для продакшена измените следующие настройки:

```env
DEBUG=False
SECRET_KEY=сгенерируйте-надежный-ключ
ALLOWED_HOSTS=ваш-домен.com,www.ваш-домен.com
CSRF_TRUSTED_ORIGINS=https://ваш-домен.com,https://www.ваш-домен.com
```

---

## Администрирование

### Команды управления

```bash
# Локально
python manage.py <command>

# В Docker
docker-compose exec django python manage.py <command>
```

### Полезные команды:

```bash
# Миграции
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations

# Статические файлы
python manage.py collectstatic
python manage.py findstatic --verbosity 2 css/style.css

# Пользователи
python manage.py createsuperuser
python manage.py changepassword <username>

# Кэш
python manage.py create_cache_table
python manage.py clear_cache

# Фоновые задачи
python manage.py rqworker default
python manage.py rqstats
```

### Резервное копирование и восстановление

```bash
# Резервное копирование базы данных
docker-compose exec postgres pg_dump -U carwager carwager > backup_$(date +%Y%m%d).sql

# Восстановление базы данных
docker-compose exec -T postgres psql -U carwager carwager < backup_file.sql

# Резервное копирование медиафайлов
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/
```

---

## Устранение неполадок

### Общие проблемы

#### 1. Ошибка подключения к PostgreSQL
```
django.db.utils.OperationalError: connection to server at "localhost" (127.0.0.1), port 5432 failed
```
**Решение:**
- Убедитесь, что PostgreSQL запущен: `sudo systemctl status postgresql`
- Проверьте настройки в `.env` файле
- Для Docker: убедитесь, что контейнер postgres запущен

#### 2. Ошибка подключения к Redis
```
redis.exceptions.ConnectionError: Error 111 connecting to localhost:6379
```
**Решение:**
- Убедитесь, что Redis запущен: `sudo systemctl status redis-server`
- Проверьте настройки в `.env` файле
- Для Docker: убедитесь, что контейнер redis запущен

#### 3. Ошибки статических файлов
```
Static file not found
```
**Решение:**
- Выполните: `python manage.py collectstatic`
- Для Docker: `docker-compose exec django python manage.py collectstatic`
- Проверьте настройки `STATIC_URL` и `STATIC_ROOT`

#### 4. WebSockets не работают
```
WebSocket connection failed
```
**Решение:**
- Убедитесь, что Daphne запущен
- Проверьте настройки `CHANNEL_LAYERS` в settings.py
- Для Docker: убедитесь, что контейнер daphne запущен

### Docker специфичные проблемы

#### 1. Контейнеры не запускаются
```bash
# Проверьте логи
docker-compose logs

# Проверьте, заняты ли порты
sudo netstat -tulpn | grep :8080
sudo netstat -tulpn | grep :5432

# Очистите Docker
docker system prune -a
docker volume prune
```

#### 2. Проблемы с volumes
```bash
# Просмотр volumes
docker volume ls

# Удаление volumes
docker volume rm carwager_postgres_data
docker volume rm carwager_redis_data

# Пересоздание volumes
docker-compose down -v
docker-compose up -d
```

#### 3. Проблемы с сетью
```bash
# Просмотр сетей
docker network ls

# Проверка подключения между контейнерами
docker-compose exec django ping postgres
docker-compose exec django ping redis
```

### Логирование

```bash
# Просмотр логов Django
docker-compose logs django --tail=100 -f

# Просмотр логов PostgreSQL
docker-compose logs postgres --tail=50

# Просмотр логов Nginx
docker-compose logs nginx --tail=50

# Просмотр логов в реальном времени
docker-compose logs -f
```

### Производительность

```bash
# Мониторинг ресур��ов
docker stats

# Проверка использования диска
docker system df

# Очистка неиспользуемых ресурсов
docker system prune -a --volumes
```

---

## Дополнительная информация

### Структура проекта
```
carwager/
├── carwager/          # Основное приложение Django
│   ├── static/       # Статические файлы
│   ├── templates/    # HTML шаблоны
│   └── ...
├── general/          # Настройки проекта
├── showbill/         # Приложение объявлений
├── auction/          # Приложение аукционов
├── chat/            # Приложение чатов
├── news/            # Приложение новостей
├── docker/          # Docker файлы
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

### Полезные ссылки
- [Django документация](https://docs.djangoproject.com/)
- [Docker документация](https://docs.docker.com/)
- [Docker Compose документация](https://docs.docker.com/compose/)
- [PostgreSQL документация](https://www.postgresql.org/docs/)
- [Redis документация](https://redis.io/documentation)

### Контакты
- Автор: Artem Sheibak <sheibakaa@gmail.com>
- LinkedIn: [Artem Sheibak](https://www.linkedin.com/in/artem-sheibak-a12923227/)

---

## Лицензия
Проект распространяется под лицензией MIT. Подробнее см. в файле LICENSE.