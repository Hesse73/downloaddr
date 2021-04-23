#!bin/sh

echo "get packages..."
sudo pip3 install django
sudo pip3 install stdiomask
sudo pip3 install json
sudo pip3 install sqlite3
sudo pip3 install hashlib
echo "create database..."

sudo python3 manage.py migrate
sudo python3 manage.py makemigrations onefile
sudo python3 manage.py migrate

echo "you can now use:>python3 manage.py runserver 0:8000 to run site."
