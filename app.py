from flask import Flask, render_template

from config import Config, ensure_storage_directories
from routes.processing_routes import processing_bp
from routes.upload_routes import upload_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    ensure_storage_directories()

    app.register_blueprint(upload_bp)
    app.register_blueprint(processing_bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host=Config.FLASK_HOST,
        port=Config.FLASK_PORT,
        debug=Config.FLASK_DEBUG,
    )
