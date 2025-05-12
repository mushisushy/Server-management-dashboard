from . import db

class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    status = db.Column(db.String(10), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    sudo = db.Column(db.Boolean, default=False)
    docker = db.Column(db.Boolean, default=False)
    home_size = db.Column(db.Integer)  # Size in MB
    registration_date = db.Column(db.String(20))
    expire_date = db.Column(db.String(20))
    server_id = db.Column(db.Integer, db.ForeignKey('server.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    groupname = db.Column(db.String(100), nullable=False)
    server_id = db.Column(db.Integer, db.ForeignKey('server.id'), nullable=False)
    users = db.relationship('User', backref='group', lazy=True, cascade="all, delete")
    __table_args__ = (db.UniqueConstraint('groupname', 'server_id', name='unique_group_per_server'),)



def get_servers():
    servers = Server.query.all()
    return [{"name": server.name, "status": server.status} for server in servers]

def get_users(server_name):
    server = Server.query.filter_by(name=server_name).first()
    if not server:
        return []
    users = User.query.filter_by(server_id=server.id).all()
    return users

def get_groups(server_name):
    server = Server.query.filter_by(name=server_name).first()
    if not server:
        return []
    groups = Group.query.filter_by(server_id=server.id).all()
    return [{"id": group.id, "groupname": group.groupname, "user_count": len(group.users)} for group in groups]



def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    else:
        print(f"User with ID {user_id} not found")


def update_expiration(user_id, new_expiration_date):
    user = User.query.get(user_id)
    if user:
        user.expire_date = new_expiration_date
        db.session.commit()
    else:
        print(f"User with ID {user_id} not found.")


def add_group_to_server(server_name, group_name):
    server = Server.query.filter_by(name=server_name).first()

    if not server:
        raise ValueError(f"Server with name '{server_name}' not found.")

    existing_group = Group.query.filter_by(groupname=group_name, server_id=server.id).first()
    if existing_group:
        raise ValueError(f"Group with name '{group_name}' already exists on server '{server_name}'.")

    new_group = Group(groupname=group_name, server_id=server.id)
    db.session.add(new_group)
    db.session.commit()



