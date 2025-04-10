import random
import re
import string
from django.contrib.auth.models import User


def generate_random_password(length=12):
    """
    Generates a random password using letters, digits, and punctuation.
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(characters) for i in range(length))


def get_next_guest_credentials():
    """
    Returns the next available guest username and email based on existing users.
    """
    guest_users = User.objects.filter(username__startswith="guest")
    max_number = 10

    for user in guest_users:
        match = re.match(r"guest(\d+)", user.username)
        if match:
            number = int(match.group(1))
            if number > max_number:
                max_number = number

    next_number = max_number + 1
    username = f"guest{next_number}"
    email = f"{username}@example.com"
    return username, email
