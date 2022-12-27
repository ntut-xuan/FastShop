from secrets import token_hex
from urllib.parse import quote

SECRET_KEY: str = token_hex()
SQLALCHEMY_DATABASE_URI: str = (
    "mysql+pymysql://fsa:{password}@mariadb:3306/fastshop".format(
        password=quote("@fsa2022")
    )
)
STATIC_RESOURCE_PATH = "/var/fastshop/image"
SWAGGER = {
    "title": "FastShop API",
    "uiversion": "3",
    "openapi": "3.0.3",
    "termsOfService": "",
    "version": "0.3.0",
    "description": "This is a FastShop API based on the OpenAPI 3.0 specification.",
}
