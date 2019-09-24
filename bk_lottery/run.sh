echo "启动抽奖程序..."
cd "$(dirname "$0")"
echo "更新/创建数据库"
python manage.py makemigrations
python manage.py migrate
echo "启动服务"
python2.7 manage.py runserver 80