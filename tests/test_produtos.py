"""Testes automatizados para os endpoints da API dos produtos."""
from unittest.mock import patch

import mysql.connector
import pytest

from tests.conftest import _mock_produto

# ---------------------------------------------------------------------------
# GET /produtos
# ---------------------------------------------------------------------------


class TestListarProdutos:
    def test_listar_retorna_lista_vazia(self, client):
        with patch("api.routes.produtos.get_all_produtos", return_value=[]):
            resp = client.get("/produtos")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["success"] is True
        assert data["data"] == []
        assert "message" in data

    def test_listar_retorna_produtos(self, client):
        produtos = [_mock_produto(1), _mock_produto(2, nome="Teclado")]
        with patch("api.routes.produtos.get_all_produtos", return_value=produtos):
            resp = client.get("/produtos")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["success"] is True
        assert len(data["data"]) == 2

    def test_listar_com_filtro_nome(self, client):
        produto = _mock_produto()
        with patch("api.routes.produtos.get_all_produtos", return_value=[produto]) as mock_fn:
            resp = client.get("/produtos?nome=Mouse")
        mock_fn.assert_called_once_with(nome="Mouse", marca=None, estoque_baixo=False)
        assert resp.status_code == 200

    def test_listar_com_filtro_marca(self, client):
        produto = _mock_produto()
        with patch("api.routes.produtos.get_all_produtos", return_value=[produto]) as mock_fn:
            resp = client.get("/produtos?marca=Logitech")
        mock_fn.assert_called_once_with(nome=None, marca="Logitech", estoque_baixo=False)
        assert resp.status_code == 200

    def test_listar_com_estoque_baixo(self, client):
        with patch("api.routes.produtos.get_all_produtos", return_value=[]) as mock_fn:
            resp = client.get("/produtos?estoque_baixo=true")
        mock_fn.assert_called_once_with(nome=None, marca=None, estoque_baixo=True)
        assert resp.status_code == 200

    def test_listar_erro_banco(self, client):
        with patch(
            "api.routes.produtos.get_all_produtos",
            side_effect=mysql.connector.Error("fail"),
        ):
            resp = client.get("/produtos")
        assert resp.status_code == 500
        data = resp.get_json()
        assert data["success"] is False


# ---------------------------------------------------------------------------
# GET /produtos/<id>
# ---------------------------------------------------------------------------


class TestBuscarProduto:
    def test_buscar_produto_existente(self, client):
        produto = _mock_produto()
        with patch("api.routes.produtos.get_produto_by_id", return_value=produto):
            resp = client.get("/produtos/1")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["success"] is True
        assert data["data"]["id"] == 1

    def test_buscar_produto_inexistente(self, client):
        with patch("api.routes.produtos.get_produto_by_id", return_value=None):
            resp = client.get("/produtos/999")
        assert resp.status_code == 404
        data = resp.get_json()
        assert data["success"] is False
        assert "errors" in data

    def test_buscar_erro_banco(self, client):
        with patch(
            "api.routes.produtos.get_produto_by_id",
            side_effect=mysql.connector.Error("fail"),
        ):
            resp = client.get("/produtos/1")
        assert resp.status_code == 500
        data = resp.get_json()
        assert data["success"] is False


# ---------------------------------------------------------------------------
# POST /produtos
# ---------------------------------------------------------------------------


class TestCriarProduto:
    def test_criar_produto_sucesso(self, client):
        with patch("api.routes.produtos.create_produto", return_value=1):
            resp = client.post(
                "/produtos",
                json={"nome": "Mouse", "preco": 50.0, "quantidade": 10},
            )
        assert resp.status_code == 201
        data = resp.get_json()
        assert data["success"] is True
        assert data["data"]["id"] == 1

    def test_criar_sem_nome(self, client):
        resp = client.post("/produtos", json={"preco": 50.0})
        assert resp.status_code == 400
        data = resp.get_json()
        assert data["success"] is False
        assert len(data["errors"]) > 0

    def test_criar_sem_preco(self, client):
        resp = client.post("/produtos", json={"nome": "Mouse"})
        assert resp.status_code == 400
        data = resp.get_json()
        assert data["success"] is False
        assert len(data["errors"]) > 0

    def test_criar_nome_vazio(self, client):
        resp = client.post("/produtos", json={"nome": "   ", "preco": 10.0})
        assert resp.status_code == 400
        data = resp.get_json()
        assert data["success"] is False

    def test_criar_preco_invalido(self, client):
        resp = client.post("/produtos", json={"nome": "Mouse", "preco": "abc"})
        assert resp.status_code == 400

    def test_criar_preco_negativo(self, client):
        resp = client.post("/produtos", json={"nome": "Mouse", "preco": -1.0})
        assert resp.status_code == 400

    def test_criar_quantidade_negativa(self, client):
        resp = client.post("/produtos", json={"nome": "Mouse", "preco": 10.0, "quantidade": -5})
        assert resp.status_code == 400

    def test_criar_sem_content_type_json(self, client):
        resp = client.post(
            "/produtos",
            data="nome=Mouse&preco=10",
            content_type="application/x-www-form-urlencoded",
        )
        assert resp.status_code == 415

    def test_criar_nome_muito_longo(self, client):
        resp = client.post("/produtos", json={"nome": "A" * 101, "preco": 10.0})
        assert resp.status_code == 400

    def test_criar_marca_muito_longa(self, client):
        resp = client.post("/produtos", json={"nome": "Mouse", "preco": 10.0, "marca": "M" * 51})
        assert resp.status_code == 400

    def test_criar_erro_banco(self, client):
        with patch(
            "api.routes.produtos.create_produto",
            side_effect=mysql.connector.Error("fail"),
        ):
            resp = client.post("/produtos", json={"nome": "Mouse", "preco": 10.0})
        assert resp.status_code == 500

    def test_resposta_padronizada_sucesso(self, client):
        """Verifica que a resposta tem as chaves: success, message, data."""
        with patch("api.routes.produtos.create_produto", return_value=42):
            resp = client.post("/produtos", json={"nome": "Teclado", "preco": 100.0})
        data = resp.get_json()
        assert "success" in data
        assert "message" in data
        assert "data" in data

    def test_resposta_padronizada_erro(self, client):
        """Verifica que a resposta de erro tem as chaves: success, message, data, errors."""
        resp = client.post("/produtos", json={"preco": 50.0})
        data = resp.get_json()
        assert "success" in data
        assert "message" in data
        assert "data" in data
        assert "errors" in data


# ---------------------------------------------------------------------------
# PUT /produtos/<id>
# ---------------------------------------------------------------------------


class TestAtualizarProduto:
    def test_atualizar_produto_sucesso(self, client):
        with patch("api.routes.produtos.update_produto", return_value=1):
            resp = client.put(
                "/produtos/1",
                json={"quantidade": 20, "preco": 45.0},
            )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["success"] is True

    def test_atualizar_produto_inexistente(self, client):
        with patch("api.routes.produtos.update_produto", return_value=0):
            resp = client.put("/produtos/999", json={"quantidade": 5, "preco": 10.0})
        assert resp.status_code == 404

    def test_atualizar_sem_quantidade(self, client):
        resp = client.put("/produtos/1", json={"preco": 10.0})
        assert resp.status_code == 400

    def test_atualizar_sem_preco(self, client):
        resp = client.put("/produtos/1", json={"quantidade": 5})
        assert resp.status_code == 400

    def test_atualizar_sem_content_type_json(self, client):
        resp = client.put(
            "/produtos/1",
            data="quantidade=5&preco=10",
            content_type="application/x-www-form-urlencoded",
        )
        assert resp.status_code == 415


# ---------------------------------------------------------------------------
# PATCH /produtos/<id>
# ---------------------------------------------------------------------------


class TestAtualizarProdutoParcial:
    def test_patch_apenas_preco(self, client):
        with patch("api.routes.produtos.patch_produto", return_value=1):
            resp = client.patch("/produtos/1", json={"preco": 99.99})
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["success"] is True

    def test_patch_apenas_quantidade(self, client):
        with patch("api.routes.produtos.patch_produto", return_value=1):
            resp = client.patch("/produtos/1", json={"quantidade": 5})
        assert resp.status_code == 200

    def test_patch_apenas_nome(self, client):
        with patch("api.routes.produtos.patch_produto", return_value=1):
            resp = client.patch("/produtos/1", json={"nome": "Novo Nome"})
        assert resp.status_code == 200

    def test_patch_sem_campos(self, client):
        resp = client.patch("/produtos/1", json={})
        assert resp.status_code == 400
        data = resp.get_json()
        assert data["success"] is False

    def test_patch_produto_inexistente(self, client):
        with patch("api.routes.produtos.patch_produto", return_value=0):
            resp = client.patch("/produtos/999", json={"preco": 10.0})
        assert resp.status_code == 404

    def test_patch_preco_invalido(self, client):
        resp = client.patch("/produtos/1", json={"preco": "nao_numero"})
        assert resp.status_code == 400

    def test_patch_sem_content_type_json(self, client):
        resp = client.patch(
            "/produtos/1",
            data="preco=10",
            content_type="application/x-www-form-urlencoded",
        )
        assert resp.status_code == 415


# ---------------------------------------------------------------------------
# DELETE /produtos/<id>
# ---------------------------------------------------------------------------


class TestDeletarProduto:
    def test_deletar_produto_sucesso(self, client):
        with patch("api.routes.produtos.delete_produto", return_value=1):
            resp = client.delete("/produtos/1")
        assert resp.status_code == 204

    def test_deletar_produto_inexistente(self, client):
        with patch("api.routes.produtos.delete_produto", return_value=0):
            resp = client.delete("/produtos/999")
        assert resp.status_code == 404
        data = resp.get_json()
        assert data["success"] is False

    def test_deletar_erro_banco(self, client):
        with patch(
            "api.routes.produtos.delete_produto",
            side_effect=mysql.connector.Error("fail"),
        ):
            resp = client.delete("/produtos/1")
        assert resp.status_code == 500
