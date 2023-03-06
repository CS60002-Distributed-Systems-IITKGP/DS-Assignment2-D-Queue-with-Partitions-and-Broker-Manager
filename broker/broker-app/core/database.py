from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker

# from core.config import settings

# POSTGRES_USER = user
# - POSTGRES_PASSWORD = password
# - POSTGRES_DB = appdb
POSTGRES_USER = 'user'
POSTGRES_PASSWORD = 'password'
POSTGRES_HOST = 'localhost'
POSTGRES_PORT = '5222'  # Change to the port number you're using
POSTGRES_DB = 'appdb'

DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
print(DATABASE_URL)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)


# engine = create_engine(settings.DATABASE_URI, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@as_declarative()
class Base:

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
