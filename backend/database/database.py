from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Reemplaza los datos con los que te dio Filess.io
# Formato: mysql+pymysql://USUARIO:PASSWORD@HOST:PUERTO/NOMBRE_BD
DATABASE_URL = "mysql+pymysql://Tienda_AGAL_lostelsewe:a70d5210da2322f4894a6a4864d04cc1a1128dad@0u6ka8.h.filess.io:3307/Tienda_AGAL_lostelsewe"

# Quitamos el connect_args={"check_same_thread": False} porque eso solo era para SQLite
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()