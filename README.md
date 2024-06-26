# Backend
It is a project to build a shopping mall backend using python.

## 관련 링크
[Front-end](https://github.com/CHWI-JI-JIG/FrontEnd)
<br>[Admin_Front](https://github.com/CHWI-JI-JIG/Admin_Front)
<br>[시연영상](https://youtu.be/BcE3djFZ35M)


# How to Start
## Downlode Code

```bash
git clone https://github.com/CHWI-JI-JIG/Backend.git
cd Backend
pip install -r requirements.txt
```

# Requirements
```bash
# python<=3.11
pip install -r requirements.txt
```  

### Make secrets.json and mysql_config.py
`secrets.json`
```json
{
    "SECRET_KEY": "YOUR_SECRET_KEY"
}
```

`mysql_config.py`
```python
mysql_db = {
    "user": "USER_NAME",
    "password": "DB_PASSWORD",
    "host": "localhost",
    "port": 3306,
    "database": "DATABASE_NAME",
    "charset": "utf8",
}
```

### How to Set MySQL
1. `download` mysql and base setting
2. `create` mysql user and database (root로 만들면, 유저관련은 생략가능)
   ```sql
    CREATE DATABASE "DATABASE_NAME" DEFAULT character SET UTF8 COLLATE utf8_general_ci;
    CREATE user "USER_NAME"@localhost identified by 'DB_PASSWORD';
    GRANT ALL PRIVILEGE on "DATABASE_NAME".* to 'USER_NAME'@'localhost';
    # GRANT ALL PRIVILEGES ON "DATABASE_NAME".* TO 'USER_NAME'@'localhost';
   ```
3. `run` manage.py (DB 테이블 생성과, 초기 계정&일기 생성)
    ```bash
    # clear db and init member
    python manage.py --run migrate --clear_db_init --init
    # just migrate
    python manage.py --run migrate
    ```

### Make mail_config.py
```python
class Mail_Config:
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USERNAME = "[YOUR_MAIL]@gmail.com"
    MAIL_PASSWORD = "[APP KEY ABOUT YOUR_MAIL]"
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER = "[YOUR_MAIL]@gmail.com"
```

### [How to Set Mail](https://roksf0130.tistory.com/126)

# How to Run
## How to Run Flask
```bash
python manage.py --run flask-main --host x.x.x.x --port 5000
python manage.py --run flask-admin --host x.x.x.x --port 5001
```

## How to Test
```bash
python manage.py --run test
```
