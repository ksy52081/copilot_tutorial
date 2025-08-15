import pytest
import os


@pytest.fixture(autouse=True)
def cleanup_db():
    """
    각 테스트 전후로 SQLite DB 파일을 삭제하여 초기화한다.
    """
    db_path = os.path.join(os.path.dirname(__file__), "..", "app", "test.db")
    if os.path.exists(db_path):
        os.remove(db_path)
    yield
    if os.path.exists(db_path):
        os.remove(db_path)
