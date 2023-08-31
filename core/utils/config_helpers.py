import json

from core.utils.secrets_manager import get_secret


def build_database_uri(
    DB_DRIVER,
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER=None,
    DB_PASSWORD=None,
):
    """
    Build DB_NAME uri from the given parameters

    :param DB_DRIVER: Database driver
    :param DB_HOST: Database host
    :param DB_PORT: Database port
    :param DB_NAME: Database name
    :param DB_USER: Database user, defaults to None
    :param DB_PASSWORD: Database password, defaults to None
    :return: Database uri
    """
    DB_CONNECTION_URI = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}" 

    if DB_USER is None and DB_PASSWORD is None:
        DB_CONNECTION_URI = f"{DB_DRIVER}://{DB_HOST}:{DB_PORT}/{DB_NAME}"

    return DB_CONNECTION_URI


def get_database_uri_from_secret(secret_key):
    """
    Get database uri from the given secret key

    :param secret_key: Secret key
    :return: Database uri
    """

    db_secrets = json.loads(get_secret(secret_key))

    db_secrets['DB_DRIVER'] = db_secrets['DB_DRIVER'] if 'DB_DRIVER' in db_secrets else 'postgresql'
    db_secrets['DB_HOST'] = db_secrets['DB_HOST'] if 'DB_HOST' in db_secrets else 'postgres'
    db_secrets['DB_PORT'] = db_secrets['DB_PORT'] if 'DB_PORT' in db_secrets else 5432
    db_secrets['DB_NAME'] = db_secrets['DB_NAME'] if 'DB_NAME' in db_secrets else 'postgres'
    db_secrets['DB_USER'] = db_secrets['DB_USER'] if 'DB_USER' in db_secrets else 'postgres'
    db_secrets['DB_PASSWORD'] = db_secrets['DB_PASSWORD'] if 'DB_PASSWORD' in db_secrets else 'postgres'


    return build_database_uri(
        DB_DRIVER=db_secrets['DB_DRIVER'],
        DB_HOST=db_secrets['DB_HOST'],
        DB_PORT=db_secrets['DB_PORT'],
        DB_NAME=db_secrets['DB_NAME'],
        DB_USER=db_secrets['DB_USER'],
        DB_PASSWORD=db_secrets['DB_PASSWORD'],
    )
