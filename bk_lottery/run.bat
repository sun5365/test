set PATH=%PATH%;C:\Python27\;C:\Python27\Scripts;C:\Program Files\Git\bin;
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 80