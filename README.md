## Dependency

 ```
$ sudo apt install -y python3-venv
$ sudo apt-get install python-dev python3-dev build-essential libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev python-pip libmysqlclient-dev wkhtmltopdf

```
#### Create virtualenv and activate
```
$ python3 -m venv my_env
$ source my_env/bin/activate
``` 

#### Install project dependency
```
$ pip3 install wheel
$ pip3 install -r requirements.txt
```

#### Run project
```
$ python run.py
```

#### API Lists
```
POST /signup
POST /signin
GET /userinfo
DELETE /signout
```