from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()

class DatabaseManager:
    """Gestionnaire de connexion à la base de données"""
    
    def __init__(self, database_uri):
        self.engine = create_engine(
            database_uri,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            echo=False
        )
        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)
        
    @contextmanager
    def get_session(self):
        """Context manager pour les sessions"""
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            session.close()
    
    def close(self):
        """Ferme toutes les connexions"""
        self.Session.remove()
        self.engine.dispose()
