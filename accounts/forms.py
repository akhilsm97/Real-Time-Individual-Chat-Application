"""
This form collects and validates user credentials required to create
a new user account.
"""

from django import forms


class RegisterForm(forms.Form):
    """
    Form for registering a new user.

    This form collects basic user information needed for account creation,
    including email address, username, and password.

    Fields:
        Fields:
        email (EmailField): User's email address. Must be a valid email format.
        username (CharField): Desired username. Maximum length is 100 characters.
        password (CharField): User's password input, shown using a password input widget.
    """

    email = forms.EmailField()
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
