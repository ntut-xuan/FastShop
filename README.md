# FastShop

## Introduction

![FastShop](https://user-images.githubusercontent.com/69747731/189900653-63525935-2691-487d-9709-1a030ff7c470.png)

FastShop，一款以 React.js + Python 為開發工具的輕量購物網站，滿足購買者與販賣者的需求。


## Repository root

```
*
|
| -- /src/           The place storage JSX File.
| -- /static/        The place storage static file like JS File, Image, css. (frontend)
| -- /backend/       The place storage backend file.
| -- database.sql    The SQL file to setup SQL Database.
| -- babel.sh        The shell to execute babel command to compile JSX File.
| -- tailwindcss.sh  The shell to execute tailwindcss command, generate CSS File to static folder.
| -- Dockerfile      The Dockerfile to setup environment.
```

## Installization

The repository use docker to setup environment.

Please use following command to build the enviromnent.

```
docker build -t fastshop
docker run -it fastshop
```

You can use VSCode-remote-plugin to connect to docker container to develope project.