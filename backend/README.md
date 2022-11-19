[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# FastShop Backend

## How to run

If you're in the `backend/` directory, the following command starts the application at port 8080.

```bash
flask run --host 0.0.0.0 --port 8080
```

> You have to create database tables for the first time.
>
> ```bash
> flask create-db
> ```

If in the `fastshop/` directory or anywhere else, specifying the path of factory function (`create_app`) will do the work.

```bash
flask --app backend/app:create_app run --host 0.0.0.0 --port 8080
```

To run the application in debug mode, add `--debug` flag to `flask`. \
*warn: do not enable debug mode when deploying in production.*

## How to test

Make sure you're in the `backend/` directory, then run the following command.

```bash
python -m pytest
```

This runs both unit and integration tests.
If you want to run only unit or integration test, append `tests/unit_tests` or `tests/integration_tests` to the command, respectively.

> note: A running `mariadb-test` container is required to run the integration tests.
