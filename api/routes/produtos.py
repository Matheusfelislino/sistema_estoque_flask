from flask import Blueprint, jsonify, request

from api.models.produto import (
    create_produto,
    delete_produto,
    get_all_produtos,
    get_produto_by_id,
    update_produto,
)

produtos_bp = Blueprint("produtos", __name__)


@produtos_bp.route("/produtos", methods=["GET"])
def listar_produtos():
    """Lista todos os produtos do estoque."""
    produtos = get_all_produtos()
    return jsonify({"success": True, "data": produtos}), 200


@produtos_bp.route("/produtos/<int:produto_id>", methods=["GET"])
def buscar_produto(produto_id):
    """Busca um produto específico pelo ID."""
    produto = get_produto_by_id(produto_id)
    if produto is None:
        return jsonify({"success": False, "error": "Produto não encontrado"}), 404
    return jsonify({"success": True, "data": produto}), 200


@produtos_bp.route("/produtos", methods=["POST"])
def criar_produto():
    """Cria um novo produto no estoque."""
    dados = request.get_json()

    if not dados:
        return jsonify({"success": False, "error": "Dados inválidos"}), 400

    if "nome" not in dados:
        return jsonify({"success": False, "error": "Campo 'nome' é obrigatório"}), 400

    if "preco" not in dados:
        return jsonify({"success": False, "error": "Campo 'preco' é obrigatório"}), 400

    try:
        preco = float(dados["preco"])
        if preco < 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"success": False, "error": "Preço inválido"}), 400

    try:
        quantidade = int(dados.get("quantidade", 0))
        if quantidade < 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"success": False, "error": "Quantidade inválida"}), 400

    novo_id = create_produto(
        nome=dados["nome"],
        marca=dados.get("marca", ""),
        preco=preco,
        quantidade=quantidade,
    )

    return (
        jsonify(
            {
                "success": True,
                "message": "Produto criado com sucesso!",
                "data": {"id": novo_id},
            }
        ),
        201,
    )


@produtos_bp.route("/produtos/<int:produto_id>", methods=["PUT"])
def atualizar_produto(produto_id):
    """Atualiza quantidade e preço de um produto."""
    dados = request.get_json()

    if not dados:
        return jsonify({"success": False, "error": "Dados inválidos"}), 400

    if "quantidade" not in dados:
        return (
            jsonify({"success": False, "error": "Campo 'quantidade' é obrigatório"}),
            400,
        )

    if "preco" not in dados:
        return jsonify({"success": False, "error": "Campo 'preco' é obrigatório"}), 400

    try:
        preco = float(dados["preco"])
        if preco < 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"success": False, "error": "Preço inválido"}), 400

    try:
        quantidade = int(dados["quantidade"])
        if quantidade < 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"success": False, "error": "Quantidade inválida"}), 400

    rows = update_produto(produto_id, quantidade, preco)

    if rows == 0:
        return jsonify({"success": False, "error": "Produto não encontrado"}), 404

    return jsonify({"success": True, "message": "Estoque atualizado com sucesso!"}), 200


@produtos_bp.route("/produtos/<int:produto_id>", methods=["DELETE"])
def deletar_produto(produto_id):
    """Remove um produto do estoque."""
    rows = delete_produto(produto_id)

    if rows == 0:
        return jsonify({"success": False, "error": "Produto não encontrado"}), 404

    return "", 204
