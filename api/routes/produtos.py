from flask import Blueprint, jsonify, request

from api.models.produto import (
    create_produto,
    delete_produto,
    get_all_produtos,
    get_produto_by_id,
    update_produto,
)

produtos_bp = Blueprint("produtos", __name__)


def error_response(message, status_code=400):
    return jsonify({"success": False, "message": message}), status_code


@produtos_bp.route("/produtos", methods=["GET"])
def listar_produtos():
    """Lista todos os produtos do estoque."""
    try:
        produtos = get_all_produtos()
        return jsonify(
            {
                "success": True,
                "message": "Produtos listados com sucesso.",
                "data": produtos,
            }
        ), 200
    except Exception:
        return error_response("Erro interno ao listar produtos.", 500)


@produtos_bp.route("/produtos/<int:produto_id>", methods=["GET"])
def buscar_produto(produto_id):
    """Busca um produto específico pelo ID."""
    try:
        produto = get_produto_by_id(produto_id)

        if produto is None:
            return error_response("Produto não encontrado.", 404)

        return jsonify(
            {
                "success": True,
                "message": "Produto encontrado com sucesso.",
                "data": produto,
            }
        ), 200
    except Exception:
        return error_response("Erro interno ao buscar produto.", 500)


@produtos_bp.route("/produtos", methods=["POST"])
def criar_produto():
    """Cria um novo produto no estoque."""
    if not request.is_json:
        return error_response("O conteúdo da requisição deve ser JSON.", 415)

    dados = request.get_json(silent=True)
    if not dados:
        return error_response("Dados inválidos ou corpo vazio.", 400)

    nome = str(dados.get("nome", "")).strip()
    marca = str(dados.get("marca", "")).strip()

    if not nome:
        return error_response("Campo 'nome' é obrigatório.", 400)

    try:
        preco = float(dados.get("preco"))
        if preco < 0:
            raise ValueError
    except (TypeError, ValueError):
        return error_response("Campo 'preco' inválido.", 400)

    try:
        quantidade = int(dados.get("quantidade", 0))
        if quantidade < 0:
            raise ValueError
    except (TypeError, ValueError):
        return error_response("Campo 'quantidade' inválido.", 400)

    try:
        novo_id = create_produto(
            nome=nome,
            marca=marca,
            preco=preco,
            quantidade=quantidade,
        )

        return jsonify(
            {
                "success": True,
                "message": "Produto criado com sucesso.",
                "data": {
                    "id": novo_id,
                    "nome": nome,
                    "marca": marca,
                    "preco": preco,
                    "quantidade": quantidade,
                },
            }
        ), 201
    except Exception:
        return error_response("Erro interno ao criar produto.", 500)


@produtos_bp.route("/produtos/<int:produto_id>", methods=["PUT"])
def atualizar_produto(produto_id):
    """Atualiza quantidade e preço de um produto."""
    if not request.is_json:
        return error_response("O conteúdo da requisição deve ser JSON.", 415)

    dados = request.get_json(silent=True)
    if not dados:
        return error_response("Dados inválidos ou corpo vazio.", 400)

    try:
        preco = float(dados.get("preco"))
        if preco < 0:
            raise ValueError
    except (TypeError, ValueError):
        return error_response("Campo 'preco' inválido.", 400)

    try:
        quantidade = int(dados.get("quantidade"))
        if quantidade < 0:
            raise ValueError
    except (TypeError, ValueError):
        return error_response("Campo 'quantidade' inválido.", 400)

    try:
        rows = update_produto(produto_id, quantidade, preco)

        if rows == 0:
            return error_response("Produto não encontrado.", 404)

        produto_atualizado = get_produto_by_id(produto_id)

        return jsonify(
            {
                "success": True,
                "message": "Produto atualizado com sucesso.",
                "data": produto_atualizado,
            }
        ), 200
    except Exception:
        return error_response("Erro interno ao atualizar produto.", 500)


@produtos_bp.route("/produtos/<int:produto_id>", methods=["DELETE"])
def deletar_produto(produto_id):
    """Remove um produto do estoque."""
    try:
        rows = delete_produto(produto_id)

        if rows == 0:
            return error_response("Produto não encontrado.", 404)

        return jsonify(
            {
                "success": True,
                "message": "Produto removido com sucesso.",
            }
        ), 200
    except Exception:
        return error_response("Erro interno ao remover produto.", 500)