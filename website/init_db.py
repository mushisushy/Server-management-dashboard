from website import create_app, db
from website.models import Server, User, Group
import pymysql

app = create_app()
app.app_context().push()


db.create_all()

if Server.query.first():
    print("ℹ️ Data already exists — skipping init.")
else:
    print("ℹ️ Populating initial database data...")

    server1 = Server(name="Server 1", status="live")
    server2 = Server(name="Server 2", status="down")
    db.session.add_all([server1, server2])
    db.session.commit()

    group1 = Group(groupname="admin", server_id=server1.id)
    group2 = Group(groupname="developers", server_id=server1.id)
    group3 = Group(groupname="marketing", server_id=server1.id)
    group4 = Group(groupname="support", server_id=server1.id)
    db.session.add_all([group1, group2, group3, group4])
    db.session.commit()

    users_server1 = [
        User(username="Иван", sudo=True, docker=True, home_size=512, registration_date="2023-11-01", expire_date="2024-11-01", server_id=server1.id, group_id=group2.id),
        User(username="Алексей", sudo=False, docker=True, home_size=1024, registration_date="2023-11-02", expire_date="2024-11-02", server_id=server1.id, group_id=group1.id),
        User(username="Мария", sudo=True, docker=False, home_size=256, registration_date="2023-11-03", expire_date="2024-11-03", server_id=server1.id, group_id=group3.id),
        User(username="Елена", sudo=False, docker=True, home_size=512, registration_date="2023-11-04", expire_date="2024-11-04", server_id=server1.id, group_id=group4.id),
        User(username="Дмитрий", sudo=True, docker=False, home_size=2048, registration_date="2023-11-05", expire_date="2024-11-05", server_id=server1.id, group_id=group1.id),
        User(username="Андрей", sudo=False, docker=True, home_size=128, registration_date="2023-11-06", expire_date="2024-11-06", server_id=server1.id, group_id=group2.id),
        User(username="Aarav", sudo=True, docker=True, home_size=512, registration_date="2023-11-07", expire_date="2024-11-07", server_id=server1.id, group_id=group4.id),
        User(username="Vikram", sudo=False, docker=False, home_size=1024, registration_date="2023-11-08", expire_date="2024-11-08", server_id=server1.id, group_id=group3.id),
        User(username="Ananya", sudo=True, docker=True, home_size=256, registration_date="2023-11-09", expire_date="2024-11-09", server_id=server1.id, group_id=group1.id),
        User(username="Riya", sudo=False, docker=False, home_size=512, registration_date="2023-11-10", expire_date="2024-11-10", server_id=server1.id, group_id=group1.id),
        User(username="Sidharth", sudo=True, docker=False, home_size=2048, registration_date="2023-11-11", expire_date="2024-11-11", server_id=server1.id, group_id=group4.id),
        User(username="آرش", sudo=False, docker=True, home_size=1024, registration_date="2023-11-12", expire_date="2024-11-12", server_id=server1.id, group_id=group4.id),
        User(username="مهدی", sudo=True, docker=False, home_size=2048, registration_date="2023-11-13", expire_date="2024-11-13", server_id=server1.id, group_id=group3.id),
        User(username="نرگس", sudo=False, docker=True, home_size=512, registration_date="2023-11-14", expire_date="2024-11-14", server_id=server1.id, group_id=group2.id),
        User(username="سارا", sudo=True, docker=False, home_size=256, registration_date="2023-11-15", expire_date="2024-11-15", server_id=server1.id, group_id=group1.id),
    ]
    db.session.add_all(users_server1)
    db.session.commit()

    group5 = Group(groupname="Admin", server_id=server2.id)
    group6 = Group(groupname="Developers", server_id=server2.id)
    group7 = Group(groupname="Marketing", server_id=server2.id)
    group8 = Group(groupname="Support", server_id=server2.id)
    db.session.add_all([group5, group6, group7, group8])
    db.session.commit()

    users_server2 = [
        User(username="John", sudo=True, docker=True, home_size=512, registration_date="2023-12-01", expire_date="2024-12-01", server_id=server2.id, group_id=group6.id),
        User(username="Michael", sudo=False, docker=True, home_size=1024, registration_date="2023-12-02", expire_date="2024-12-02", server_id=server2.id, group_id=group5.id),
        User(username="Sarah", sudo=True, docker=False, home_size=256, registration_date="2023-12-03", expire_date="2024-12-03", server_id=server2.id, group_id=group7.id),
        User(username="Emma", sudo=False, docker=True, home_size=512, registration_date="2023-12-04", expire_date="2024-12-04", server_id=server2.id, group_id=group8.id),
        User(username="David", sudo=True, docker=False, home_size=2048, registration_date="2023-12-05", expire_date="2024-12-05", server_id=server2.id, group_id=group5.id),
        User(username="Sophia", sudo=False, docker=True, home_size=128, registration_date="2023-12-06", expire_date="2024-12-06", server_id=server2.id, group_id=group6.id),
        User(username="Arjun", sudo=True, docker=True, home_size=512, registration_date="2023-12-07", expire_date="2024-12-07", server_id=server2.id, group_id=group8.id),
        User(username="Rajesh", sudo=False, docker=False, home_size=1024, registration_date="2023-12-08", expire_date="2024-12-08", server_id=server2.id, group_id=group7.id),
        User(username="Priya", sudo=True, docker=True, home_size=256, registration_date="2023-12-09", expire_date="2024-12-09", server_id=server2.id, group_id=group5.id),
        User(username="Aditi", sudo=False, docker=False, home_size=512, registration_date="2023-12-10", expire_date="2024-12-10", server_id=server2.id, group_id=group5.id),
        User(username="Siddharth", sudo=True, docker=False, home_size=2048, registration_date="2023-12-11", expire_date="2024-12-11", server_id=server2.id, group_id=group8.id),
        User(username="Ali", sudo=False, docker=True, home_size=1024, registration_date="2023-12-12", expire_date="2024-12-12", server_id=server2.id, group_id=group8.id),
        User(username="Mona", sudo=True, docker=False, home_size=2048, registration_date="2023-12-13", expire_date="2024-12-13", server_id=server2.id, group_id=group7.id),
        User(username="Omid", sudo=False, docker=True, home_size=512, registration_date="2023-12-14", expire_date="2024-12-14", server_id=server2.id, group_id=group6.id),
        User(username="Leila", sudo=True, docker=False, home_size=256, registration_date="2023-12-15", expire_date="2024-12-15", server_id=server2.id, group_id=group5.id),
    ]
    db.session.add_all(users_server2)
    db.session.commit()

    print("✅ Data successfully added!")
