import os
from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from functools import wraps
from dotenv import load_dotenv

load_dotenv()


def get_engine_for_port(port, database=None):
    return create_engine('postgresql://{user}:{password}@{host}:{port}/{db}'.format(
        user=os.getenv('PGUSER'),
        password=os.getenv('PGPASSWORD'),
        host=os.getenv('PGHOST'),
        port=port,
        db=database or os.getenv('PGDATABASE'),
    ), pool_pre_ping=True)


def with_sql_session(function, args, kwargs, engine=None):
    if engine is None:
        # Default to local port
        engine = get_engine_for_port(5433)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        return function(session, *args, **kwargs)
    finally:
        session.close()


def backtest_sql_session(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        engine = get_engine_for_port(5433, 'backtesting')
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            return function(session, *args, **kwargs)
        finally:
            session.close()

    return wrapper


def with_local_sql_session(function, *args, **kwargs):
    return with_sql_session(function, args, kwargs)


def with_remote_sql_session(function, *args, **kwargs):
    # Hat tip: https://stackoverflow.com/a/38001815
    with SSHTunnelForwarder(
            (os.getenv('DB_SERVER_ADDRESS'), 22),
            ssh_username=os.getenv('DB_SERVER_USERNAME'),
            ssh_pkey=os.getenv('DB_SERVER_SSH_KEY_PATH'),
            remote_bind_address=('127.0.0.1', 5433)
    ) as tunnel:
        tunnel.start()
        engine = get_engine_for_port(tunnel.local_bind_port)
        return with_sql_session(function, args, kwargs, engine=engine)


# Decorators
def local_sql_session(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        return with_local_sql_session(function, *args, **kwargs)
    return wrapper


def remote_sql_session(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        return with_remote_sql_session(function, *args, **kwargs)
    return wrapper


def sql_session(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        # reuse session
        if len(args) > 0 and isinstance(args[0], Session):
            return function(args[0], *(args[1:]), **kwargs)
        # remote session
        if os.getenv('PYTHON_ENV') == 'staging':
            return with_remote_sql_session(function, *args, **kwargs)
        # local session
        else:
            return with_local_sql_session(function, *args, **kwargs)
    return wrapper
