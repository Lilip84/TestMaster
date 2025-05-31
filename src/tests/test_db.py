from sqlalchemy import create_engine, text

def test_database_connection():
    engine = create_engine("sqlite:///test.db")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.scalar() == 1

def test_user_count():
    engine = create_engine("sqlite:///test.db")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM users"))
        count = result.scalar()
        assert count > 0