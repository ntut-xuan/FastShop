# FastShop

## Introduction

![FastShop](https://user-images.githubusercontent.com/69747731/189900653-63525935-2691-487d-9709-1a030ff7c470.png)

FastShop，一款以 React.js + Python 為開發工具的輕量購物網站，滿足購買者與販賣者的需求。


## Repository root

```
*
|
| -- /src/              The directory storage JSX File.
| -- /static/           The directory storage static file like JS File, Image, css. (frontend)
| -- /backend/          The directory storage backend file.
| -- /html/             The directory storage HTML file.
| -- database.sql       The SQL file to setup SQL Database.
| -- babel.sh           The shell to execute babel command to compile JSX File.
| -- tailwindcss.sh     The shell to execute tailwindcss command, generate CSS File to static folder.
| -- Dockerfile         The Dockerfile to setup environment.
| -- docker-compose.yml The Docker compose file to setup multiple container.
```

## Installization

The repository use docker to setup environment.

Please use the following command to build the enviromnent.

```
docker compose up
```

You can use the following command to force-rebuild the environment if any changes on Dockerfile are made.

But it will setup more slowly.

```
docker compose up --build --force-recreate --no-deps
```

You can use VSCode-remote-plugin to connect docker-container to develope project.
