#!bin/sh

echo "get packages..."
sudo pip3 install django, stdiomask, json, sqlite3, hashlib
echo "create database..."

sudo rm -rf onefile/migrations/
sudo python3 manage.py migrate
sudo python3 manage.py makemigrations
sudo python3 manage.py migrate

echo "you can now use:>python3 manage.py runserver 0:8000 to run site."