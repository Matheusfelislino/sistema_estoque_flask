"""Configuração do Pytest e fixtures compartilhadas.

Os testes são executados na aplicação Flask real, mas simulam a camada do modelo de banco de dados para que nenhuma conexão real com o MySQL seja necessária na integração contínua.

"""
from unittest.mock import MagicMock, patch

import pytest

from api import create_app


@pytest.fixture()
def app():
    """Cria a aplicação Flask configurada para testes."""
    application = create_app()
    application.config["TESTING"] = True
    return application


@pytest.fixture()
def client(app):
    """Retorna um cliente de teste para a aplicação."""
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
    """Retorna um dicionário representando uma linha de produto."""
    return {
        "id": id,
        "nome": nome,
        "marca": marca,
        "preco": preco,
        "quantidade": quantidade,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00",
    }
