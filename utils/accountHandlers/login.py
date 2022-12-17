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

        if not bcrypt.verify(password, user_info.Password):
            cursor.rollback()
            cursor.close()
            return jsonify(error="Password does not match!")

        user = {
            "id": user_info.Id,
            "email": user_info.Email,
            "username": user_info.Username
        }

        cursor.close()
        return jsonify(user), 200

    except Exception as e:
        cursor.close()
        return jsonify(error="Error"), 400
