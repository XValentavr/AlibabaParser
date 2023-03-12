from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.helpers.project_envs import ProjectEnvs

engine = create_engine(ProjectEnvs.POSTGRESQL_HOST)
connection = engine.connect()

Session = sessionmaker()
Session.configure(bind=engine)

session = Session()
