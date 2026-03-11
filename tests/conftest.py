"""Pytest configuration and shared fixtures.

Tests run against the real Flask application but mock the database model
layer so that no actual MySQL connection is required in CI.
"""
from unittest.mock import MagicMock, patch

import pytest

from api import create_app


@pytest.fixture()
def app():
    """Create the Flask application configured for testing."""
    application = create_app()
    application.config["TESTING"] = True
    return application


@pytest.fixture()
def client(app):
    """Return a test client for the application."""
    return app.test_client()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _mock_produto(
    id: int = 1,
    nome: str = "Mouse",
    marca: str = "Logitech",
    preco: float = 50.0,
    quantidade: int = 10,
):
    """Return a dict representing a produto row."""
    return {
        "id": id,
        "nome": nome,
        "marca": marca,
        "preco": preco,
        "quantidade": quantidade,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00",
    }
