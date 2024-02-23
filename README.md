# Backend
It is a project to build a shopping mall backend using python.

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

### Make secrets.json and db_config.py
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
    "port": "3306",
    "database": "DATABASE_NAME",
    "charset": "utf8",
}
```

### Set MySQL
1. `download` mysql and base setting
2. `create` mysql user and database (root로 만들면, 유저관련은 생략가능)
   ```sql
    create database "DATABASE_NAME";
    create user "USER_NAME"@localhost identified by 'DB_PASSWORD';
    grant all privilege on "DATABASE_NAME".* to 'USER_NAME'@'localhost';
   ```
3. `run` manage.py (DB 테이블 생성과, 초기 계정&일기 생성)
    ```bash
    python manage.py --run migrate
    ```

# How to Run
## How to Run Django
```bash
python Django/manage.py --runserver 
```

## How to Test
```bash
python manage.py --run test
```