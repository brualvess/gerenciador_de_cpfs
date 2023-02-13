from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine("sqlite:///data.db")
Session = sessionmaker(bind=engine)

Base = declarative_base()

## test database session
test_engine = create_engine("sqlite:///test.db")
Test_session = sessionmaker(bind=test_engine)
