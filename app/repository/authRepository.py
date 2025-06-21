from sqlalchemy import text
from app.db import db
from sqlalchemy.exc import SQLAlchemyError

def find_admin(username, password):
    select_sql = text("""
    SELECT username, password FROM admin WHERE admin.username = :username AND admin.password = :password
    """)
    result = db.session.execute(select_sql, {
        "username" : username,
        "password" : password
    }).first()
    if not result:
        return False
    return True

def get_admin():
    select_sql = text("""
        SELECT username FROM admin LIMIT 1
    """)
    result = db.session.execute(select_sql).first()
    return result._mapping['username'] if result else None

def get_admin_pass():
    select_sql = text("""
        SELECT password FROM admin LIMIT 1
    """)
    result = db.session.execute(select_sql).first()
    return result._mapping['password'] if result else None

def find(username, password):
    select_sql = text("""
    SELECT username, password FROM app_user WHERE app_user.username = :username AND app_user.password = :password
    """)
    result = db.session.execute(select_sql, {
        "username" : username,
        "password" : password
    }).first()
    if not result:
        return False
    return True

def findIfUsernameTaken(username):
    select_sql = text("""
        SELECT username FROM app_user WHERE app_user.username = :username
    """)
    result = db.session.execute(select_sql, {"username": username}).first()
    if result:
        return True
    return False


def add(username, password):
    insert_sql = text("""
        INSERT INTO app_user (username, password, role) VALUES (:username, :password, :role)
    """)
    try:
        db.session.execute(insert_sql, {
            "username": username,
            "password": password,
            "role": 'user'
        })
        db.session.commit()  # This is necessary to save the changes
        return True
    except SQLAlchemyError as e:
        db.session.rollback()  # Revert any changes on error
        return False