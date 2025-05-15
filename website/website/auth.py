from flask import Blueprint, flash, redirect, render_template, request, url_for

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "admin" and password == "password":
            flash("Login successful!")
            return redirect(url_for("main.home"))
        else:
            flash("Invalid credentials, try again.")
    return render_template("login.html")
