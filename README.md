# FastShop

## Introduction

![FastShop](https://user-images.githubusercontent.com/69747731/189900653-63525935-2691-487d-9709-1a030ff7c470.png)

FastShop，一款以 React.js + Python 為開發工具的輕量購物網站，滿足購買者與販賣者的需求。

## Repository root

```
*
|
| -- /src/              JSX files.
| -- /static/           Static files like JS files, images, and CSS. (frontend)
| -- /backend/          Backend files.
| -- /html/             HTML files.
| -- database.sql       SQL files to set up the database.
| -- babel.sh           The babel commands for compiling JSX files.
| -- tailwindcss.sh     The tailwindcss commands for generating CSS files to the static folder.
| -- Dockerfile         The environment setups in docker.
| -- docker-compose.yml The environment setups of multiple containers.
```

## Installation

The repository use docker to set up the environment.

Please use the following command to build the environment.

```bash
docker compose up
```

You can use the following command to force-rebuild the environment if any changes on Dockerfile are made.

But it will be set up more slowly.

```bash
docker compose up --build --force-recreate --no-deps
```

You can use VSCode-remote-plugin to connect the docker-container to the develop project.

## Contribution

Install the Git hook scripts with the following command.

```bash
pre-commit install
```
