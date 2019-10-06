# to-do-list-api
Simple to-do list api on DRF


![travis-ci](https://travis-ci.org/gladunvv/to-do-list-api.svg?branch=master)

### Краткое описание:
Простое API для создания блокнота-задачника, реализован полный CRUD функционал, есть регистрация через токены, 
отправка письма на почтовый ящик при регистрации, возможность добавлять новые задачи, у задач есть приоритет выполнения 
(low, normal, high), дата и время создания, есть возможность задать дату напоминания, в будущем планируется отправлять напоминания 
на email при подтверждении, а так-же с помощью push-уведомлений.

### Requirements:
+ Django==2.2.5
+ django-debug-toolbar==2.0
+ djangorestframework==3.10.3
+ coverage==4.5.4
+ pytz==2019.2
+ sqlparse==0.3.0
+ yapf==0.28.0


### Сборка и запуск:
```
git clone git@github.com:gladunvv/to-do-list-api.git
cd to-do-list-api
pip install virtualenv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd app/
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```


### License
This project is licensed under the terms of the MIT license