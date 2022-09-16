[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# FastShop Backend

## How to run

If you're in the `backend/` directory, the following command starts the application at port 8080.

```
flask run --host 0.0.0.0 --port 8080
```

If in the `fastshop/` directory or anywhere else, specifying the path of factory function (`create_app`) will do the work.

```
flask --app backend/app:create_app run --host 0.0.0.0 --port 8080
```


## How to test

Make sure you're in the `backend/` directory, then run the following command.

```
python -m pytest
```
