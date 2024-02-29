import re

from app.models.account import ACTIVE_ACCOUNT, SUSPENDED_ACCOUNT
from app.models.loan_application import (
    PENDING_LOAN,
    APPROVED_LOAN,
    REJECTED_LOAN,
    SUBMETED_LOAN,
)
from app.models.role import ADMIN_ROLE, CLIENT_ROLE
from app.models.transaction import (
    TRANSFER_TRANSACTION,
    DEPOSIT_TRANSACTION,
    WITHDRAWAL_TRANSACTION,
)


email_regex = re.compile(
    r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])"
)


def is_valid_email(email):
    """
    Validates an email address based on a regular expression and additional checks.

    Args:
      email (str): The email address to validate.

    Returns:
      bool: True if the email is valid, False otherwise.
    """

    if not re.fullmatch(email_regex, email):
        return False

    return True


roles_set = set([ADMIN_ROLE, CLIENT_ROLE])


def is_valid_role(user_role):
    return user_role in roles_set


account_set = set([ACTIVE_ACCOUNT, SUSPENDED_ACCOUNT])


def is_valid_account_status(account_status):
    return account_status in account_set


loan_set = set([PENDING_LOAN, APPROVED_LOAN, REJECTED_LOAN, SUBMETED_LOAN])


def is_valid_loan_status(loan_status):
    return loan_status in loan_set


transaction_set = set(
    [TRANSFER_TRANSACTION, DEPOSIT_TRANSACTION, WITHDRAWAL_TRANSACTION]
)


def is_valid_transaction_type(transaction_type):
    return transaction_type in transaction_set
