from database import Base, engine

# Models need to be imported here in order to create the tables
from models import User, Rooftop, Project  # noqa


def create_tables():
    Base.metadata.create_all(bind=engine)
