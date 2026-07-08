from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db_url = settings.DATABASE_URL
connect_args = {}

# Handle SQLite threading check if SQLite URL is specified
if db_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False

try:
    # Attempt to initialize database engine
    engine = create_engine(db_url, connect_args=connect_args)
    # Test connection immediately to catch errors early
    with engine.connect() as conn:
        logger.info(f"Successfully connected to database: {db_url.split('@')[-1] if '@' in db_url else db_url}")
except Exception as e:
    logger.warning(
        f"Database connection failed with URL '{db_url}'. "
        f"Error: {e}. Falling back to local SQLite database for offline/development mode."
    )
    # Fall back to SQLite database file
    fallback_url = "sqlite:///./weekly_reports.db"
    connect_args = {"check_same_thread": False}
    engine = create_engine(fallback_url, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to yield database sessions to FastAPI endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
