from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker

DATABASE_URL="postgresql://postgres:159951@localhost/fastapi_db"

engine=create_engine(DATABASE_URL)

SessionaLocal=sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

Base=declarative_base()

# from sqlalchemy import create_engine

# DATABASE_URL="postgresql://postgress:password@localhos/fastapi_db"

# engine=create_engine(DATABASE_URL)

# SessionaLocal=sessionmaker(
#     bind=engine,
#     autoflush=False,
#     autocommit=False
# )
# Base=declarative_base()