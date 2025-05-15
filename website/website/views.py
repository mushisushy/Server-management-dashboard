import datetime

from flask import Blueprint, render_template, url_for, redirect, request, jsonify

from website.website import db
from website.website.models import get_servers, get_users, get_groups, delete_user, update_expiration, add_group_to_server, User, \
    Server, Group


main_page = Blueprint("main_page", __name__)


@main_page.route("/")
def index():
    servers = get_servers()
    return render_template("main.html", servers=servers)


@main_page.route("/users/<server_name>")
def list_users(server_name):
    users = get_users(server_name)
    return render_template("users.html", server_name=server_name, users=users)


@main_page.route("/groups/<server_name>")
def list_groups(server_name):
    groups = get_groups(server_name)
    return render_template("groups.html", server_name=server_name, groups=groups)


@main_page.route("/signup/<server_name>", methods=["GET", "POST"])
def signup(server_name):
    if request.method == "POST":
        username = request.form.get("name")
        password = request.form.get("password")
        group_name = request.form.get("group")
        sudo = bool(request.form.get("sudo"))
        docker = bool(request.form.get("docker"))
        expire_date = request.form.get("expiration")

        server = Server.query.filter_by(name=server_name).first()
        if not server:
            return "Server not found", 404

        existing_user = User.query.filter_by(username=username, server_id=server.id).first()
        if existing_user:
            return "User already exists", 400

        group = None
        if group_name:
            group = Group.query.filter_by(groupname=group_name, server_id=server.id).first()
            if not group:
                return "Group not found", 404

        # Create the user
        new_user = User(
            username=username,
            sudo=sudo,
            docker=docker,
            home_size=None,
            registration_date=datetime.datetime.now().strftime('%Y-%m-%d'),
            expire_date=expire_date,
            server_id=server.id,
            group_id=group.id if group else None
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('main_page.list_users', server_name=server_name))

    return render_template("signup.html", server_name=server_name)


@main_page.route("/group_users/<server_name>/<int:group_id>")
def group_users(server_name, group_id):
    group_users = User.query.filter_by(server_id=Server.query.filter_by(name=server_name).first().id, group_id=group_id).all()

    if not group_users:
        return render_template("group_users.html",
                               server_name=server_name,
                               group_id=group_id,
                               users=[],
                               message="No users found in this group.")

    return render_template("group_users.html", server_name=server_name, group_id=group_id, users=group_users)



@main_page.route("/delete_user/<int:user_id>/<server_name>", methods=["GET"])
def delete_user_route(user_id, server_name):
    delete_user(user_id)
    return redirect(url_for('main_page.list_users', server_name=server_name))


@main_page.route("/change_expiration/<int:user_id>/<server_name>", methods=["GET", "POST"])
def change_expiration(user_id, server_name):
    if request.method == "POST":
        new_expiration_date = request.form.get("expiration_date")
        update_expiration(user_id, new_expiration_date)
        return redirect(url_for('main_page.list_users', server_name=server_name))

    return render_template("change_expiration.html", user_id=user_id,
                           server_name=server_name)

@main_page.route("/add_group/<server_name>", methods=["POST"])
def add_group(server_name):
    group_name = request.form.get("group_name")

    if group_name:
        add_group_to_server(server_name, group_name)

    return redirect(url_for('main_page.list_groups', server_name=server_name))


@main_page.route("/add_users/<server_name>/<int:group_id>", methods=["GET", "POST"])
def add_users_to_group(server_name, group_id):
    if request.method == "POST":
        selected_users = request.json.get("users", [])
        print("Selected users received:", selected_users)

        group = Group.query.filter_by(id=group_id, server_id=Server.query.filter_by(name=server_name).first().id).first()
        db.session.commit()
        if not group:
            return {"error": "Group not found."}, 404

        for username in selected_users:
            user = User.query.filter_by(username=username, server_id=group.server_id).first()
            if user and user.group_id != group_id:
                user.group_id = group_id

        db.session.commit()

        return {"message": "Users added successfully."}, 200

    users = get_users(server_name)
    return render_template(
        "add_user.html",
        server_name=server_name,
        group_id=group_id,
        users=users
    )


@main_page.route("/delete_group/<server_name>/<int:group_id>", methods=["GET"])
def delete_group(server_name, group_id):
    group = Group.query.get(group_id)
    if group:
        for user in group.users:
            user.group_id = None
        db.session.delete(group)
        db.session.commit()
        return redirect(url_for('main_page.list_groups', server_name=server_name))
    else:
        return "Group not found", 404


@main_page.route("/toggle_sudo/<int:user_id>", methods=["POST"])
def toggle_sudo(user_id):
    # Fetch the user
    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found"}, 404

    user.sudo = not user.sudo
    db.session.commit()

    return {"message": "Sudo status updated", "sudo": user.sudo}, 200

@main_page.route("/toggle_docker/<int:user_id>", methods=["POST"])
def toggle_docker(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found"}, 404

    user.docker = not user.docker
    db.session.commit()

    return {"message": "Docker status updated", "docker": user.docker}, 200


@main_page.route("/change_password/<int:user_id>", methods=["POST"])
def change_password(user_id):
    new_password = request.form.get("new_password")
    if not new_password:
        return {"error": "Password cannot be empty"}, 400


    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found"}, 404

    user.password = new_password
    db.session.commit()

    return jsonify({"message": "Password updated successfully"}), 200

