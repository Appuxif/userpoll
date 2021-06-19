# userpoll
API для системы опросов пользователей

## Deploy

### Common

* Скопировать config.ini.template в config.ini
* Установить свои переменные в config.ini (не обязательно для lite)

### Docker lite 
Простой запуск через docker  
Использует manage.py runserver

* Зависимости
    * Docker
        * https://www.digitalocean.com/community/tutorials/docker-ubuntu-18-04-1-ru
        * https://docs.docker.com/engine/install/ubuntu/
        * https://docs.docker.com/docker-for-windows/install/

* Запустить приложение
    * `$ docker-compose -f docker-compose-lite.yml up`
    
* Доступ по адресу http://localhost:8083
        
### Docker
Запуск через docker

* Зависимости
    * Docker
        * https://www.digitalocean.com/community/tutorials/docker-ubuntu-18-04-1-ru
        * https://docs.docker.com/engine/install/ubuntu/
        * https://docs.docker.com/docker-for-windows/install/

* Настроить сервер в папке ./_server
    * Поместить сертификаты в ./_server/nginx/cert
    * Настроить конфиг nginx в ./_server/nginx/conf.d
    
* Запустить приложение
    * `$ docker-compose up`

* Доступ по адресу https://www.example.com


### Local
Запуск локально

* Зависимости
    * python3.7.9
    * python3-venv
    * PostgreSQL

* `$ python3 -m venv venv`
* `$ ./venv/bin/python -m pip install -r requirements.txt`
* `$ ./venv/bin/python manage.py makemigrations`
* `$ ./venv/bin/python manage.py migrate`
* `$ ./venv/bin/python manage.py createsuperuser`


* `$ ./venv/bin/python manage.py runserver 0.0.0.0:8083`  
или  
* `$ ./venv/bin/gunicorn --access-logfile - --workers 1 --timeout 30 --bind unix:./webapp.sock webapp.wsgi:application`

# Info
Задача: спроектировать и разработать API для системы опросов пользователей.

Функционал для администратора системы:

- авторизация в системе (регистрация не нужна)
- добавление/изменение/удаление опросов. Атрибуты опроса: название, дата старта, дата окончания, описание. После создания поле "дата старта" у опроса менять нельзя
- добавление/изменение/удаление вопросов в опросе. Атрибуты вопросов: текст вопроса, тип вопроса (ответ текстом, ответ с выбором одного варианта, ответ с выбором нескольких вариантов)

Функционал для пользователей системы:

- получение списка активных опросов
- прохождение опроса: опросы можно проходить анонимно, в качестве идентификатора пользователя в API передаётся числовой ID, по которому сохраняются ответы пользователя на вопросы; один пользователь может участвовать в любом количестве опросов
- получение пройденных пользователем опросов с детализацией по ответам (что выбрано) по ID уникальному пользователя

Использовать следующие технологии: Django 2.2.10, Django REST framework.

Результат выполнения задачи:
- исходный код приложения в github (только на github, публичный репозиторий)
- инструкция по разворачиванию приложения (в docker или локально)
- документация по API