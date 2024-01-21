
<!-- markdownlint-disable MD032 MD033-->
# 🔥 **CustomAFK GitHub Template next app**

<!-- <p align="center"> -->
<!--   <br> -->
<!--   <a href="https://github.com/QuangPhamvt/ie307-front-end-next/issues"> -->
<!--     <img src="https://img.shields.io/github/issues-closed/QuangPhamvt/ie307-front-end-next?color=0088ff&style=for-the-badge&logo=github" alt="@QuangPhamvt/ie307-front-end's issues"/> -->
<!--   </a> -->
<!--   <a href="https://github.com/QuangPhamvt/ie307-front-end-next/pulls"> -->
<!--     <img src="https://img.shields.io/github/issues-pr-closed/QuangPhamvt/ie307-front-end-next?color=0088ff&style=for-the-badge&logo=github" alt="@QuangPhamvt/project-template's pull requests"/> -->
<!--   </a> -->
<!--   <a href="https://github.com/QuangPhamvt/ie307-front-end-next/actions/workflows/deploy.yml"> -->
<!--     <img src="https://github.com/QuangPhamvt/ie307-front-end-next/actions/workflows/deploy.yml/badge.svg" alt="@QuangPhamvt/ie307-front-end-next's tests"> -->
<!--   </a> -->
<!-- </p> -->

---

## 🤔 **What is this project?**

* This is API website for e-commerce

---

## ⚡ **Installation**

1. Prerequires
- python version > 3.11.x
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

## 📚 **What does it include?**


---

### 🌲 **Project tree**

```
```

---

## 📝 **Additional notes**

## 📖 **Information**
### Package
```
    [packages]
    fastapi = "*"
    uvicorn = {extras = ["standard"], version = "*"}
    pymysql = "*"
    pydantic = "*"
    strawberry-graphql = {extras = ["fastapi"], version = "*"}
    asyncmy = "*"
    sqlalchemy = {extras = ["asyncio"], version = "*"}

    [dev-packages]
    ruff = "*"
    pre-commit = "*"
    rich = "*"
    typer = "*"
    libcst = "*"
    alembic = "*"
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
