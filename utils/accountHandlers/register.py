from flask import jsonify
from email_validator import validate_email, EmailNotValidError
from passlib.hash import bcrypt


def register(email, username, password, db_connection):
    # Validate user data
    try:
        validate_email(email)
    except EmailNotValidError:
        return jsonify(error="Invalid Email!"), 400

    cursor = db_connection.cursor()

    try:
        # Retrieve user email from database
        cursor.execute("SELECT email "
                       "FROM Users "
                       f"WHERE email ='{email}' "
                       f"OR username = '{username}'")

        if cursor.rowcount != 0:
            cursor.close()
            return jsonify(error="This account is already registered!"), 400

        cursor.execute("INSERT INTO Users (email, username, password) "
                       f"VALUES ('{email}', '{username}', '{bcrypt.using(rounds=12, ident='2b').hash(password)}')")

        # Close Connection
        cursor.commit()
        cursor.close()
        return jsonify(success="User created!"), 200

    except Exception:
        cursor.rollback()
        cursor.close()
        return jsonify(error="Error"), 400
