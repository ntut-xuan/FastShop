import pymysql


def connect_database() -> pymysql.Connection:
    conn = pymysql.connect(
        host="fastshop-mariadb-1",
        user="fsa",
        password="@fsa2022",
        database="fastshop",
    )
    return conn
