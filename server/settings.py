from envparse import Env

env = Env()

DATABASE_URL = env.str(
    "DATABASE_URL",
    default="postgresql+asyncpg://gen_user:d|yUIbDU153MG{@grand-db.ayarayarovich.tech:5432/default_db",
)
