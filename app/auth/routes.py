from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from datetime import datetime
from ..extensions import db
from ..models import User
from ..validators import validate_email, validate_username, validate_password

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form_data = {"username": "", "email": ""}
    errors = {}

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        form_data = {"username": username, "email": email}

        if not username:
            errors["username"] = True
        if not email:
            errors["email"] = True
        if not password:
            errors["password"] = True
        if not confirm:
            errors["confirm_password"] = True

        if errors:
            flash("Please fill all the gaps", "error")
            return render_template("register.html", form=form_data, errors=errors)

        ok, msg = validate_username(username)
        if not ok:
            errors["username"] = True
            flash(msg, "error")
            return render_template("register.html", form=form_data, errors=errors)

        ok, msg = validate_email(email)
        if not ok:
            errors["email"] = True
            flash(msg, "error")
            return render_template("register.html", form=form_data, errors=errors)

        ok, msg = validate_password(password)
        if not ok:
            errors["password"] = True
            flash(msg, "error")
            return render_template("register.html", form=form_data, errors=errors)

        if password != confirm:
            errors["confirm_password"] = True
            flash("Passwords do not match", "error")
            return render_template("register.html", form=form_data, errors=errors)

        if User.query.filter_by(username=username).first():
            errors["username"] = True
            flash("Username taken", "error")
            return render_template("register.html", form=form_data, errors=errors)

        if User.query.filter_by(email=email).first():
            errors["email"] = True
            flash("Email taken", "error")
            return render_template("register.html", form=form_data, errors=errors)

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Registration successful", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form_data, errors=errors)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form_data = {"username": ""}
    errors = {}

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        form_data = {"username": username}

        if not username:
            errors["username"] = True
        if not password:
            errors["password"] = True

        if errors:
            flash("Please fill all the gaps", "error")
            return render_template("login.html", form=form_data, errors=errors)

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            if user.is_account_locked():
                flash("Account temporarily locked", "error")
                return render_template("login.html", form=form_data, errors=errors)

            if not user.is_active:
                flash("Account deactivated", "error")
                return render_template("login.html", form=form_data, errors=errors)

            user.reset_failed_attempts()
            user.last_login = datetime.utcnow()
            db.session.commit()

            login_user(user)
            flash("Login successful", "success")
            return redirect(url_for("dashboard"))

        if user:
            user.increment_failed_attempts()
            db.session.commit()

        errors["username"] = True
        errors["password"] = True
        flash("Invalid username or password", "error")
        return render_template("login.html", form=form_data, errors=errors)

    return render_template("login.html", form=form_data, errors=errors)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out", "info")
    return redirect(url_for("auth.login"))

