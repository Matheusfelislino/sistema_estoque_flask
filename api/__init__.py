from flask import Flask, jsonify


def create_app():
    """Cria e configura a aplicação Flask."""
    app = Flask(__name__)

    from api.routes.produtos import produtos_bp
    app.register_blueprint(produtos_bp)

    @app.route("/")
    def home():
        return jsonify(
            {
                "success": True,
                "message": "API de Estoque rodando com sucesso.",
                "endpoints": {
                    "listar_produtos": "/produtos",
                    "buscar_produto": "/produtos/<id>",
                },
            }
        ), 200

    return app