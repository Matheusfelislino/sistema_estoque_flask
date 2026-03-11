from flask import Flask


def create_app():
    """Cria e configura a aplicação Flask."""
    app = Flask(__name__)

    from api.routes.produtos import produtos_bp
    app.register_blueprint(produtos_bp)

    @app.route("/")
    def home():
        return (
            "<h1>API de Estoque Rodando!</h1>"
            "<p>Acesse <a href='/produtos'>/produtos</a> para ver a lista.</p>"
        )

    return app
