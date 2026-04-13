from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 

# URL de conexion a MYSQL
DATABASE_URL = "mysql+pymsql://root:@localhost:3306/ecommerce_db"

# crear conexion a la base de datos
engine = create_engine(DATABASE_URL, echo=True)

# crear sesiones para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False, 
                            bind=engine
                            )
# Base para los modelos de la base de datos
Base = declarative_base() 