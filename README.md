#  Социальная сеть для публикации личных дневников.
* **Описание**: Социальная сеть для публикации личных дневников. Пользователь может создать свою страницу и публиковать на ней посты. 
Для каждого поста муожно указать категорию и локацию. Пользователи могут заходить на чужие страницы, читать и комментировать чужие посты.
* **Стек технологий**  
  Django, Bootstrap5, Pillow, HTML
* **Установка**  
Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:KatyaSoloveva/django_sprint4.git
```  

```
cd django_sprint4
```
Создать и активировать виртуальное окружение:
```
python -m venv venv
```

Для Windows
```
source venv/Scripts/activate
```

Для Linux
```
source venv/bin/activate
```
Загрузить зависимости
```
pip install -r requirements.txt
```
```
python -m pip install --upgrade pip
```
Перейти в директорию blogicum, выполнить миграции, загрузить фикстуры в БД и запустить проект:
```
python manage.py makemigrations
python manage.py migrate
```
```
python manage.py loaddata db.json
```
```
python manage.py runserver
```

* **Created by Ekaterina Soloveva**  
https://github.com/KatyaSoloveva
