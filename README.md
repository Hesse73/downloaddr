# Downloaddr
A very small download server using django

Get packages and set database(`sqlite3`):
```
bash install.sh
```

Run server:
```
python3 manage.py runserver 0:port
```

Add/clear files for users(identified by account name):
```
python3 addFile.py
python3 clearFile.py
```

### TODO

 - support for multi-threaded download
 - uploading from browser(which is not safe)
 - file encryption
