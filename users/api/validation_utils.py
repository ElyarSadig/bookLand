import re


def is_username_valid(username):
    # Check if the username contains only letters, numbers, underscores, or hyphens
    if not re.match("^[a-zA-Z0-9_-]*$", username):
        return False

    # Check if the username is between 4 and 30 characters in length
    if not 3 <= len(username) <= 30:
        return False

    return True


def is_email_valid(email):
    # Define a regular expression pattern for a valid email address
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Check if the email matches the pattern
    if re.match(email_pattern, email):
        return True
    else:
        return False


def password_match(password, password2):
    return password == password2


def is_password_valid(password):
    error_message = ""
    if len(password) < 8:
        error_message = "رمز عبور باید حداقل ۸ کاراکتر باشد"

    # At least one uppercase letter
    if not any(char.isupper() for char in password):
        error_message = "رمز عبور باید حداقل یک حرف بزرگ داشته باشد"

    # At least one lowercase letter
    if not any(char.islower() for char in password):
        error_message = "رمز عبور باید حداقل یک حرف کوچک داشته باشد"

    # At least one digit
    if not any(char.isdigit() for char in password):
        error_message = "رمز عبور باید حداقل دارای یک رقم باشد"

    # At least one special character
    if not re.search(r"[!@#$%^&*()-_=+{}|;:,.<>/?`~]", password):
        error_message = "رمز عبور باید حداقل یک کاراکتر خاص داشته باشد"

    return error_message


def validate_iranian_phone_number(phone_number):
    pattern = r'^0\d{10}$'

    if re.match(pattern, phone_number):
        return True
    else:
        return False


def is_valid_iranian_bank_card(card_number):
    # Remove any spaces or non-digit characters
    card_number = ''.join(filter(str.isdigit, card_number))

    # Check if the length is valid
    if len(card_number) != 16:
        return False

    # Check if the format matches common Iranian bank card formats
    if not card_number.startswith('6037') and not card_number.startswith('6278'):
        return False

    # Apply the Luhn algorithm (modulus 10 algorithm) for further validation
    total = 0
    reverse_digits = card_number[::-1]

    for i in range(len(reverse_digits)):
        digit = int(reverse_digits[i])

        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9

        total += digit

    return total % 10 == 0

