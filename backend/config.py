from secrets import token_hex
from urllib.parse import quote

SECRET_KEY: str = token_hex()
SQLALCHEMY_DATABASE_URI: str = (
    "mysql+pymysql://fsa:{password}@mariadb:3306/fastshop".format(
        password=quote("@fsa2022")
    )
)
