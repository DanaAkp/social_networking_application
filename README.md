Backend приложения "SocialNetworkingApp"
---------------------

## Стек технологий

* Python 3.11
* FastApi
* python-jose
* PostgreSQL
* docker

## Шаги для запуска API

1. Клонировать текущий репозиторий.
2. Зайти в директорию скачанного репозитория.
3. Скопировать файл .env.example в файл .env и выставить нужные Вам значения переменных.
4. Выполнить команду (необходима установка docker):
   ```
   docker compose up -d
   ```
5. В браузере открыть страницу http://localhost:8080/docs с документацией в формате OpenAPI.
6. После запуска создается пользователь по умолчанию со
   следующими входными данными:
    ```
    {
        "email": "default@default.com",
        "password": "default_password"
    }
    ```

