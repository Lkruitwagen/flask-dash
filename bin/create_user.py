#!/usr/bin/env python
import getpass
from werkzeug.security import generate_password_hash

import click
from flaskdash import db, create_app
from flaskdash.models import User


@click.command()
@click.argument("username", type=click.STRING)
@click.argument("email", type=click.STRING)
def create_user(username, email):
    """
    Create a new user with USERNAME and EMAIL as provided, e.g.
    ./create_user.py john john@example.py
    """

    print(
        f"This will create a new user with the following details"
        f"\n\tUsername: {username}\n\tEmail: {email}"
        f"\n\nPlease provide a secure password."
    )
    password = getpass.getpass()
    if len(password) < 8:
        exit("A minimum of 8 characters is required for a password.")
    password_verify = getpass.getpass()
    if password != password_verify:
        exit("ERROR: Passwords must match.")

    try:
        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
        )
        db.session.add(new_user)
        db.session.commit()
    except Exception:
        exit("ERROR: Could not add user to the database")

    print("User created")


if __name__ == "__main__":
    app = create_app()
    app.app_context().push()
    db.init_app(app)
    create_user()