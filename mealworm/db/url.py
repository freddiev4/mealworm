from os import getenv


def get_db_url() -> str:
    db_driver = getenv("DB_DRIVER", "postgresql+psycopg")
    db_user = getenv("DB_USER", "ai")
    db_pass = getenv("DB_PASS", "ai")
    db_host = getenv("DB_HOST", "pgvector")
    db_port = getenv("DB_PORT", "5432")
    db_database = getenv("DB_DATABASE", "ai")
    return "{}://{}{}@{}:{}/{}".format(
        db_driver,
        db_user,
        f":{db_pass}" if db_pass else "",
        db_host,
        db_port,
        db_database,
    )
