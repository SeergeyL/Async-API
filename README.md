# Проект 

Сервис API, покрытый тестами, онлайн кинотеатра

## Стек технологий

- FastApi
- PostgreSQL
- Elasticsearch
- Redis
- Nginx
- Docker

## Запуск проекта

Клонировать репозиторий и перейти в него в командной строке:
```git
git clone https://github.com/SeergeyL/Async-API-sprint-2
```
```git
cd fastapi-solution
```

В корневой папке необходимо создать файл **.env** и заполнить переменные окружения 
по примеру файла **.env.example**

Запустить docker-compose:
```
docker-compose up -d --build
```
