import sqlalchemy as sa
import sqlalchemy.orm as orm
import psycopg2
import dotenv
import os

SqlAlchemyBase = orm.declarative_base()
__factory = None


def global_init():
    global __factory
    if __factory:
        return
    conn_str = f"postgresql+psycopg2://{os.environ.get('PGUSER')}:{os.environ.get('PGPASSWORD')}@" \
               f"{os.environ.get('PGHOST')}:{os.environ.get('PGPORT')}/{os.environ.get('PGDATABASE')}"
    # print(conn_str)
    print(os.listdir("Api"))
    engine = sa.create_engine(conn_str, echo=True)

    __factory = orm.sessionmaker(bind=engine)

    import data.__all_models
    SqlAlchemyBase.metadata.create_all(engine)


def create_session():
    global __factory
    return __factory()
