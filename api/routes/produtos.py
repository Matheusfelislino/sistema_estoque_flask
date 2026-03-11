import logging

import mysql.connector
from flask import Blueprint, jsonify, request

from api.models.produto import (
    create_produto,
    delete_produto,
    get_all_produtos,
    get_produto_by_id,
    patch_produto,
    update_produto,
)
from api.validators.produto_validator import (
    validate_create,
    validate_patch,
    validate_update,
)

produtos_bp = Blueprint("produtos", __name__)
logger = logging.getLogger(__name__)


def _error_response(message: str, errors: list, status: int):
    """Helper que monta uma resposta de erro padronizada."""
    return (
        jsonify({"success": False, "message": message, "data": None, "errors": errors}),
        status,
    )


def _require_json():
    """Retorna uma resposta de erro se o Content-Type não for application/json."""
    if not request.is_json:
        return _error_response(
            "Content-Type deve ser application/json",
            ["Header 'Content-Type: application/json' não encontrado"],
            415,
        )
    return None


@produtos_bp.route("/produtos", methods=["GET"])
def listar_produtos():
    """Lista todos os produtos do estoque, com filtros opcionais."""
    nome = request.args.get("nome")
    marca = request.args.get("marca")
    estoque_baixo_str = request.args.get("estoque_baixo", "false").lower()
    estoque_baixo = estoque_baixo_str == "true"

    try:
        produtos = get_all_produtos(nome=nome, marca=marca, estoque_baixo=estoque_baixo)
    except mysql.connector.Error:
        return _error_response("Erro interno ao consultar produtos", [], 500)

    return (
        jsonify({"success": True, "message": "Produtos listados com sucesso", "data": produtos}),
        200,
    )


@produtos_bp.route("/produtos/<int:produto_id>", methods=["GET"])
def buscar_produto(produto_id):
    """Busca um produto específico pelo ID."""
    try:
        produto = get_produto_by_id(produto_id)
    except mysql.connector.Error:
        return _error_response("Erro interno ao buscar produto", [], 500)

    if produto is None:
        return _error_response(
            "Produto não encontrado",
            [f"Nenhum produto com id={produto_id}"],
            404,
        )
    return (
        jsonify({"success": True, "message": "Produto encontrado", "data": produto}),
        200,
    )


@produtos_bp.route("/produtos", methods=["POST"])
def criar_produto():
    """Cria um novo produto no estoque."""
    content_type_error = _require_json()
    if content_type_error:
        return content_type_error

    dados = request.get_json(silent=True)
    if dados is None:
        return _error_response("Body JSON inválido ou ausente", ["Não foi possível parsear o JSON"], 400)

    errors = validate_create(dados)
    if errors:
        return _error_response("Dados inválidos", errors, 400)

    nome = dados["nome"].strip()
    marca = dados.get("marca", "") or ""
    preco = float(dados["preco"])
    quantidade = int(dados.get("quantidade", 0))

    try:
        novo_id = create_produto(nome=nome, marca=marca, preco=preco, quantidade=quantidade)
    except mysql.connector.Error:
        return _error_response("Erro interno ao criar produto", [], 500)

    return (
        jsonify(
            {
                "success": True,
                "message": "Produto criado com sucesso",
                "data": {"id": novo_id},
            }
        ),
        201,
    )


@produtos_bp.route("/produtos/<int:produto_id>", methods=["PUT"])
def atualizar_produto(produto_id):
    """Substitui completamente quantidade e preço de um produto (atualização completa)."""
    content_type_error = _require_json()
    if content_type_error:
        return content_type_error

    dados = request.get_json(silent=True)
    if dados is None:
        return _error_response("Body JSON inválido ou ausente", ["Não foi possível parsear o JSON"], 400)

    errors = validate_update(dados)
    if errors:
        return _error_response("Dados inválidos", errors, 400)

    quantidade = int(dados["quantidade"])
    preco = float(dados["preco"])

    try:
        rows = update_produto(produto_id, quantidade, preco)
    except mysql.connector.Error:
        return _error_response("Erro interno ao atualizar produto", [], 500)

    if rows == 0:
        return _error_response(
            "Produto não encontrado",
            [f"Nenhum produto com id={produto_id}"],
            404,
        )

    return (
        jsonify({"success": True, "message": "Produto atualizado com sucesso", "data": None}),
        200,
    )


@produtos_bp.route("/produtos/<int:produto_id>", methods=["PATCH"])
def atualizar_produto_parcial(produto_id):
    """Atualiza parcialmente um ou mais campos de um produto."""
    content_type_error = _require_json()
    if content_type_error:
        return content_type_error

    dados = request.get_json(silent=True)
    if dados is None:
        return _error_response("Body JSON inválido ou ausente", ["Não foi possível parsear o JSON"], 400)

    errors = validate_patch(dados)
    if errors:
        return _error_response("Dados inválidos", errors, 400)

    fields: dict = {}
    if "nome" in dados:
        fields["nome"] = dados["nome"].strip()
    if "marca" in dados:
        fields["marca"] = dados["marca"]
    if "preco" in dados:
        fields["preco"] = float(dados["preco"])
    if "quantidade" in dados:
        fields["quantidade"] = int(dados["quantidade"])

    try:
        rows = patch_produto(produto_id, fields)
    except mysql.connector.Error:
        return _error_response("Erro interno ao atualizar produto", [], 500)

    if rows == 0:
        return _error_response(
            "Produto não encontrado",
            [f"Nenhum produto com id={produto_id}"],
            404,
        )

    return (
        jsonify({"success": True, "message": "Produto atualizado parcialmente com sucesso", "data": None}),
        200,
    )


@produtos_bp.route("/produtos/<int:produto_id>", methods=["DELETE"])
def deletar_produto(produto_id):
    """Remove um produto do estoque."""
    try:
        rows = delete_produto(produto_id)
    except mysql.connector.Error:
        return _error_response("Erro interno ao deletar produto", [], 500)

    if rows == 0:
        return _error_response(
            "Produto não encontrado",
            [f"Nenhum produto com id={produto_id}"],
            404,
        )

    return "", 204
