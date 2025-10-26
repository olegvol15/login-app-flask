from flask import Flask, render_template
from .config import Config
from .extensions import db, login_manager, csrf
from .models import User
from .auth.routes import auth_bp
from flask_login import login_required, current_user

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    with app.app_context():
        db.create_all()
    app.register_blueprint(auth_bp)
    @app.route("/")
    def index():
        return render_template("index.html")
    @app.route("/dashboard")
    @login_required
    def dashboard():
        return render_template("dashboard.html")
    return app
