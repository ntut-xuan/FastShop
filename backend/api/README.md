# FastShop API

## Description

FastShop API is an API documentation based on the [OpenAPI 3.0 specification](https://swagger.io/specification/). The API documentation page generates by [Flasgger](https://github.com/flasgger/flasgger).

You can add the YAML file to describe the API, load the YAML file in a specific route with the `swag_from` decorator, and it should present the description in the following link:

```
http://localhost:8080/apidocs
```

## Notice

The YAML file should follow OpenAPI 3.0 specification.

Furthermore, in this project, we ask the API should follow [REST](https://zh.wikipedia.org/zh-tw/%E8%A1%A8%E7%8E%B0%E5%B1%82%E7%8A%B6%E6%80%81%E8%BD%AC%E6%8D%A2) also.
