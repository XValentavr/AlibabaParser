from os.path import dirname as d
from os.path import abspath, join
import sys

root_dir = join(d(d(abspath(__file__))), "src")
sys.path.append(root_dir)

from helpers.project_envs import ProjectEnvs
from models.base_model import Base
from models import alibaba_source_model
from models import amazon_source_model
from models import most_similar_model
from models import similarity_model
from models import url_model
from models import videos_model
from models import product_keywords
from models import alibaba_product_ids
from models import average_price

from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

config = context.config

fileConfig(config.config_file_name)

target_metadata = Base.metadata

url = ProjectEnvs.POSTGRESQL_HOST


def run_migrations_offline():
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        {"sqlalchemy.url": url},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
