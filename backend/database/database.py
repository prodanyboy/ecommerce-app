from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

DATABASE_URL = "mysql+pymysql://Tienda_AGAL_lostelsewe:a70d5210da2322f4894a6a4864d04cc1a1128dad@0u6ka8.h.filess.io:3307/Tienda_AGAL_lostelsewe"

engine = create_engine(DATABASE_URL, poolclass=NullPool)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()