import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Docker'dan gelen DATABASE_URL değişkenini okur, yoksa yerel gelişim için sqlite kullanır
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tracemark.db")

connect_args = {}
# Sadece sqlite kullanıyorsak the thread ayarını kapatmamız gerekir
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=connect_args
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

