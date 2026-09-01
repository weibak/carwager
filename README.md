# CarWager - Auto Realization and Auction Platform

## О проекте
CarWager - современная платформа для продажи автомобилей и проведения аукционов. Проект построен на Django с использованием PostgreSQL, Redis, WebSockets (Django Channels) и Docker.

**Автор:** Artem Sheibak <sheibakaa@gmail.com>

## Быстрый старт

### Варианты запуска:
1. **Локальный запуск (без Docker)** - для разработки и тестирования
2. **Запуск с Docker** - для быстрого развертывания
3. **Запуск с Docker Compose** - для production-окружения

### Требования:
- Python 3.8+
- PostgreSQL 12+
- Redis 6+
- Docker 20.10+ (для Docker варианта)
- Docker Compose 2.0+ (для Docker Compose)

## 📖 Подробные инструкции

Для подробных инструкций по каждому варианту запуска смотрите:

- **[README_LOCAL_DOCKER.md](README_LOCAL_DOCKER.md)** - Полное руководство по запуску
  - Локальный запуск (без Docker)
  - Запуск с Docker
  - Запуск с Docker Compose
  - Настройка окружения
  - Администрирование
  - Устранение неполадок

## 🚀 Краткая инструкция

### Локальный запуск (рекомендуется для разработки):
```bash
# Установка зависимостей
sudo apt install -y python3.8 python3.8-venv postgresql redis-server

# Настройка базы данных
sudo -u postgres psql -c "CREATE DATABASE carwager;"
sudo -u postgres psql -c "CREATE USER carwager WITH PASSWORD 'carwager';"

# Настройка проекта
python3.8 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Миграции и запуск
python manage.py migrate
python manage.py runserver
```

### Запуск с Docker Compose (рекомендуется для production):
```bash
# Клонирование и запуск
git clone <repository-url>
cd carwager
docker-compose build
docker-compose up -d

# Настройка базы данных
docker-compose exec django python manage.py migrate
docker-compose exec django python manage.py createsuperuser
```

## 🌐 Доступ к приложению

После запуска:
- **Основное приложение:** http://localhost:8000 (локально) или http://localhost:8080 (Docker)
- **Админ-панель:** http://localhost:8000/admin
- **WebSocket endpoint:** ws://localhost:8001/ws/

## 📁 Структура проекта

```
carwager/
├── carwager/          # Основное Django приложение
│   ├── static/       # Статические файлы (CSS, JS, изображения)
│   ├── templates/    # HTML шаблоны
│   └── ...
├── general/          # Настройки проекта
├── showbill/         # Приложение объявлений
├── auction/          # Приложение аукционов
├── chat/            # Приложение чатов (WebSocket)
├── news/            # Приложение новостей
├── docker/          # Docker конфигурации
├── docker-compose.yml
├── requirements.txt
└── README_LOCAL_DOCKER.md  # Полное руководство
```

## 🔧 Технологический стек

- **Backend:** Django 4.0, Django REST Framework
- **База данных:** PostgreSQL
- **Кэш и очереди:** Redis, Django RQ
- **WebSockets:** Django Channels, Daphne
- **Фронтенд:** Bootstrap 5, JavaScript, jQuery
- **Сервер:** Nginx, Gunicorn, Daphne
- **Контейнеризация:** Docker, Docker Compose
- **Шрифты:** Frank Ruhl Libre

## 📞 Контакты и поддержка

- **Автор:** Artem Sheibak
- **Email:** sheibakaa@gmail.com
- **LinkedIn:** [Artem Sheibak](https://www.linkedin.com/in/artem-sheibak-a12923227/)

## 📄 Лицензия

Проект распространяется под лицензией MIT. Подробнее см. в файле LICENSE.