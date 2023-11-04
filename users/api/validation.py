import re


def validate_username(username):
    # Check if the username contains only letters, numbers, underscores, or hyphens
    if not re.match("^[a-zA-Z0-9_-]*$", username):
        return False

    # Check if the username is between 4 and 30 characters in length
    if not 3 <= len(username) <= 30:
        return False

    return True


def validate_email(email):
    # Define a regular expression pattern for a valid email address
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Check if the email matches the pattern
    if re.match(email_pattern, email):
        return True
    else:
        return False