import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

from config import Config
from models import db
from routes.auth import auth_bp
from routes.posts import posts_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    app.register_blueprint(auth_bp)
    app.register_blueprint(posts_bp)

    # ── Serve uploaded images ─────────────────────────────────────────────
    @app.route("/static/uploads/<filename>")
    def uploaded_file(filename):
        upload_folder = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
        return send_from_directory(upload_folder, filename)

    # ── Health check ──────────────────────────────────────────────────────
    @app.route("/health")
    def health():
        return jsonify({"status": "ok", "message": "Blog API is running 🚀"}), 200

    # ── Error handlers ────────────────────────────────────────────────────
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"error": "Method not allowed"}), 405

    @app.errorhandler(500)
    def internal_error(e):
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500

    # ── Create tables ─────────────────────────────────────────────────────
    with app.app_context():
        db.create_all()
        # Make sure uploads folder exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        print("✅ Database tables created / verified.")

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    print("🚀 Starting Flask Blog API on http://127.0.0.1:5000")
    app.run(debug=True, host="0.0.0.0", port=port)
