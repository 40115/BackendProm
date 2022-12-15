from flask import jsonify
from email_validator import validate_email, EmailNotValidError
from passlib.hash import bcrypt


def login(email, password, db_connection):
    # Validate user data
    try:
        validate_email(email)
    except EmailNotValidError:
        return jsonify(error="Invalid Email!"), 400

    cursor = db_connection.cursor()

    try:
        # Retrieve user email from database
        cursor.execute("SELECT Id, Email, Password, Username "
                       "FROM Users "
                       f"WHERE Email ='{email}'")

        if cursor.rowcount == 0:
            cursor.close()
            return jsonify(error="User is not registered!"), 400

        user_info = cursor.fetchone()

        if not bcrypt.verify(password, user_info.password):
            cursor.rollback()
            cursor.close()
            return jsonify(error="Password does not match!")

        user = {
            "id": user_info.id,
            "email": user_info.email,
            "username": user_info.username
        }

        cursor.close()
        return jsonify(user), 200

    except Exception:
        cursor.close()
        return jsonify(error="Error"), 400
