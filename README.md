
# 🔥 **GitHub Project ECOMMERCE API**

---

## 🤔 **What is this project?**

* This is API website for e-commerce

---

## ⚡ **Installation**

1. Prerequires
- python version > 3.11.x
- Install pipenv
- Config .env file
   ```bash
   # Database
   # This is example to connect to database is localhost
   # IF use Docker compose, you can use db as host
    DB_USERNAME=root
    DB_PASSWORD=12345678
    DB_HOST=localhost
    DB_NAME=ECOMMERCE
   #Email
    RESEND_KEY=
    VERIFY_PATH=
    RESEND_SENDER=
   #Verify Token
    VERIFY_EMAIL_SECRET=
    VERIFY_EMAIL_EXPIRE=
   # Access Token
    ACCESS_TOKEN_SECRET=
    ACCESS_TOKEN_EXPIRE=
   # REFRESH TOKEN
    REFRESH_TOKEN_SECRET=
    REFRESH_TOKEN_EXPIRE=
   # Forgot Password
    FORGOT_CODE_EXPIRE=
   #AWS ACCESS KEY
    AWS_ACCESS_KEY_ID=
    AWS_SECRET_ACCESS_KEY=
   ```
2. Clone repository
   ```bash
   git clone git@github.com:QuangPhamvt/e-commerce-api.git
   ```
3. Install packages
   ```bash
   pipenv install
   ```
4. Install prepare config
   ```bash
   pre-commit install
   ```
6. Usage
   ```bash
   pipenv run server
   ```
---

## Usage Docker compose
0. Prerequires
- Install Docker
- Install Docker compose version > 2.45.x

1. Setup environment (config .env file)
   ```bash
   # Database
   # This is example to connect to database is localhost
   # IF use Docker compose, you can use db as host
    DB_USERNAME=root
    DB_PASSWORD=lunas
    DB_HOST=db
    DB_NAME=ECOMMERCE
   #Email
    RESEND_KEY=
    VERIFY_PATH=
    RESEND_SENDER=
   #Verify Token
    VERIFY_EMAIL_SECRET=
    VERIFY_EMAIL_EXPIRE=
   # Access Token
    ACCESS_TOKEN_SECRET=
    ACCESS_TOKEN_EXPIRE=
   # REFRESH TOKEN
    REFRESH_TOKEN_SECRET=
    REFRESH_TOKEN_EXPIRE=
   # Forgot Password
    FORGOT_CODE_EXPIRE=
   #AWS ACCESS KEY
    AWS_ACCESS_KEY_ID=
    AWS_SECRET_ACCESS_KEY=
   ```
2. Docker compose
   ```bash
   docker compose up
   ```
3. Check mysql database
   ```bash
   mysql -h 0.0.0.0 -P 3007 -D ECOMMERCE  -u root -p
   ```
4. Backup database
   ```bash
   mysql -h 0.0.0.0 -P 3007 -D ECOMMERCE  -u root -p >> import.sql
   ```

## 📚 **What does it include?**


---

### 🌲 **Project tree**

```
├── Dockerfile             # Docker file for build image
├── Pipfile                # Pipfile for manage package
├── Pipfile.lock           # Pipfile.lock for manage package version
├── README.md              # README.md file for project information
├── alembic                # Alembic for manage database migration
├── alembic.ini            # Alembic config file
├── app                    # App folder
│   ├── __init__.py        # Init file for app
│   ├── configs            # Configs folder for app example: database, email, token ...
│   ├── database           # Database folder for app eg: models, schemas, crud ...
│   ├── dependencies       # Dependencies folder for app eg: token, email, verify, logger, ...
│   ├── main.py            # Main file for app
│   ├── middlewares        # Middlewares folder for app eg: token, logger, ...
│   ├── routers            # Routers folder for app eg: user, product, auth, ...
│   ├── schemas            # Schemas folder for app eg: user, product, auth, ...
│   ├── services           # Services folder for app eg: user, product, auth, ...
│   └── utils              # Utils folder for app eg: token, email, verify, logger, ...
├── buildspec.yml          # Buildspec file for AWS CodeBuild CI/CD
├── docker-compose.yml     # Docker compose file for build image
├── import.sql             # Import sql file for database
├── requirements.txt       # Requirements file for manage package
└── ruff.toml              # Ruff file for manage test
```

---

## 📝 **Additional notes**
This project is licensed under the MIT License.

---
## 📖 **Information**
### Package
```
[packages]
fastapi = "*"
pymysql = "*"
asyncmy = "*"
sqlalchemy = {extras = ["asyncio"], version = "*"}
uvicorn = "*"
python-dotenv = "*"
cryptography = "*"
bcrypt = "*"
pydantic = {extras = ["email"], version = "*"}
resend = "*"
pyjwt = "*"
greenlet = "*"
boto3 = "*"
alembic = "*"

[dev-packages]
ruff = "*"
pre-commit = "*"
rich = "*"
typer = "*"
libcst = "*"
```
**requirements.txt**
```
-i https://pypi.org/simple
alembic==1.13.1; python_version >= '3.8'
annotated-types==0.6.0; python_version >= '3.8'
anyio==4.3.0; python_version >= '3.8'
asyncmy==0.2.9; python_version >= '3.7' and python_version < '4.0'
bcrypt==4.1.2; python_version >= '3.7'
boto3==1.34.66; python_version >= '3.8'
botocore==1.34.66; python_version >= '3.8'
certifi==2024.2.2; python_version >= '3.6'
cffi==1.16.0; platform_python_implementation != 'PyPy'
charset-normalizer==3.3.2; python_full_version >= '3.7.0'
click==8.1.7; python_version >= '3.7'
cryptography==42.0.5; python_version >= '3.7'
dnspython==2.6.1; python_version >= '3.8'
email-validator==2.1.1
fastapi==0.110.0; python_version >= '3.8'
greenlet==3.0.3; python_version >= '3.7'
h11==0.14.0; python_version >= '3.7'
idna==3.6; python_version >= '3.5'
jmespath==1.0.1; python_version >= '3.7'
mako==1.3.2; python_version >= '3.8'
markupsafe==2.1.5; python_version >= '3.7'
pycparser==2.21
pydantic[email]==2.6.4; python_version >= '3.8'
pydantic-core==2.16.3; python_version >= '3.8'
pyjwt==2.8.0; python_version >= '3.7'
pymysql==1.1.0; python_version >= '3.7'
python-dateutil==2.9.0.post0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'
python-dotenv==1.0.1; python_version >= '3.8'
requests==2.31.0; python_version >= '3.7'
resend==0.8.0; python_version >= '3.7'
s3transfer==0.10.1; python_version >= '3.8'
six==1.16.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'
sniffio==1.3.1; python_version >= '3.7'
sqlalchemy[asyncio]==2.0.28; python_version >= '3.7'
starlette==0.36.3; python_version >= '3.8'
typing-extensions==4.10.0; python_version >= '3.8'
urllib3==2.2.1; python_version >= '3.8'
uvicorn[standard]==0.29.0; python_version >= '3.8'
```


## ❔ **How to push**

- Role commit
  `{type}: {subject}`
  - type: build | chore | ci | docs | feat | fix | perf | refactor | revert | style | test
  - subject: 'Write a short, imperative tense description of the change'
- Automatic: check lint and format pre-commit

- Example:

```bash
git commit -m "{type}: {subject}"
```

Description
|**Types**| **Description** |
|:---| :--- |
|feat| A new feature|
|fix| A bug fix|
|docs| Documentation only changes|
|style| Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc) |
|refactor| A code change that neither fixes a bug nor adds a feature |
|perf| A code change that improves performance |
|test| Adding missing tests or correcting existing tests |
|build| Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm) |
|ci| 'Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs) |
|chore| Other changes that don't modify src or test files |
|revert| Reverts a previous commit |
