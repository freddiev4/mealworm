"""Initialize database with tables for authentication and user preferences."""

from sqlalchemy import create_engine
from mealworm.db.models import Base
from mealworm.db.url import get_db_url


def init_db():
    """Create all tables in the database."""
    db_url = get_db_url()
    print(f"Connecting to database: {db_url}")

    engine = create_engine(db_url)

    print("Creating tables...")
    Base.metadata.create_all(bind=engine)

    print("✓ Database tables created successfully!")
    print("Tables created:")
    for table in Base.metadata.sorted_tables:
        print(f"  - {table.name}")


if __name__ == "__main__":
    init_db()
