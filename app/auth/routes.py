from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from ..extensions import db
from ..models import User
from ..validators import validate_email, validate_username, validate_password

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username","").strip()
        email = request.form.get("email","").strip().lower()
        password = request.form.get("password","")
        confirm = request.form.get("confirm_password","")
        ok, msg = validate_username(username)
        if not ok:
            flash(msg, "error")
            return render_template("register.html")
        ok, msg = validate_email(email)
        if not ok:
            flash(msg, "error")
            return render_template("register.html")
        ok, msg = validate_password(password)
        if not ok:
            flash(msg, "error")
            return render_template("register.html")
        if password != confirm:
            flash("Passwords do not match", "error")
            return render_template("register.html")
        if User.query.filter_by(username=username).first():
            flash("Username taken", "error")
            return render_template("register.html")
        if User.query.filter_by(email=email).first():
            flash("Email taken", "error")
            return render_template("register.html")
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username","").strip()
        password = request.form.get("password","")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            if user.is_account_locked():
                flash("Account temporarily locked", "error")
                return render_template("login.html")
            if not user.is_active:
                flash("Account deactivated", "error")
                return render_template("login.html")
            user.reset_failed_attempts()
            user.last_login = datetime.utcnow()
            db.session.commit()
            login_user(user)
            flash("Login successful", "success")
            return redirect(url_for("dashboard"))
        else:
            if user:
                user.increment_failed_attempts()
                db.session.commit()
            flash("Invalid username or password", "error")
            return render_template("login.html")
    return render_template("login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out", "info")
    return redirect(url_for("auth.login"))
