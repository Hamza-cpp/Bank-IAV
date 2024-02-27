import re


def is_valid_email(email):
    """
    Validates an email address based on a regular expression and additional checks.

    Args:
      email (str): The email address to validate.

    Returns:
      bool: True if the email is valid, False otherwise.
    """

    # Regular expression for email validation
    email_regex = r"(^[-!#$%&'*+/=?^_`{|}~a-zA-Z0-9]+(\.[-!#$%&'*+/=?^_`{|}~a-zA-Z0-9]+)*@[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.[a-zA-Z]{2,}$)"

    # Check if email matches the regular expression
    if not re.match(email_regex, email):
        return False

    # Additional checks:
    # - Non-empty domain name
    if len(email.split("@")[-1]) == 0:
        return False
    # - At least one character before "@"
    if len(email.split("@")[0]) == 0:
        return False

    return True
