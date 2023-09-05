import pytest
from pytest_alembic.config import Config
from pytest_mock_resources import create_postgres_fixture
from alembic import command

from app.config import settings

DB_TEST_URL = (
    f"postgresql://"
    f"{settings.DB_USERNAME}:{settings.DB_PASSWORD}@"
    f"{settings.DB_HOSTNAME}:{settings.DB_PORT}/"
    f"{settings.DB_TEST_NAME}"
)


@pytest.fixture
def alembic_config():
    """Override this fixture to configure the exact alembic context setup required."""
    return Config(
        config_options={"script_location": "alembic", "sqlalchemy_url": DB_TEST_URL}
    )


@pytest.fixture
def alembic_engine():
    """Override this fixture to provide pytest-alembic powered tests with a database handle."""
    return create_postgres_fixture()


@pytest.fixture
def create_drop_test_db(alembic_config):
    command.upgrade(alembic_config, "head")
