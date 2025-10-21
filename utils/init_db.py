from database import Base, engine
#Models need to be imported here in order to create the tables
from models import User

def create_tables():
    Base.metadata.create_all(bind=engine)