""" 
    Views for user authentication and account management.

    This module has views that handle user sign up

    login and log out for the accounts app.

    The views here are, for:

    * User registration

    * User login

    * User logout

"""
from accounts.forms import RegisterForm
from accounts.models import CustomUser
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

# Define your views here ....


def register_view(request):
    """
        Handle user registration.

        Displays the registration form on GET requests and processes

        user registration on POST requests. Validates that the provided

        email and username are unique before creating a new user.

        Args:

        request (HttpRequest): The incoming HTTP request.

        Returns:

        HttpResponse: Renders the registration template on failure or GET,

        or redirects to the login page on successful registration.

        Side Effects:

        - Creates a new CustomUser record on successful form submission.

        - Adds success or error messages to the message framework.

    """
    form = RegisterForm()

    if request.method == "POST":
        if CustomUser.objects.filter(email=request.POST["email"]).exists():
            messages.error(request, "Email is already exist ...")
        elif CustomUser.objects.filter(username=request.POST["username"]).exists():
            messages.error(request, "Username is not available ...")
        else:
            form = RegisterForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data["email"]
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                CustomUser.objects.create_user(
                    username=username, email=email, password=password, is_online=False
                )
                messages.success(request, "Profile Created Successfully.")
                return redirect("accounts:login")

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    """

        Authenticate and log in a user.

        Handles user login by validating credentials submitted via POST.

        On successful authentication, logs the user in and updates their

        online status.

        Args:

        request (HttpRequest): The incoming HTTP request.

        Returns:

        HttpResponse: Renders the login template on GET or failed login,

        or redirects to the user list page on successful login.

        Side Effects:

        - Updates the user's online status.

        - Creates a login session for the authenticated user.

        - Adds success or error messages to the message framework.

    """
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user:
            user.is_online = True
            user.save()
            login(request, user)
            messages.success(
                request, f"Login successfully for {request.POST['username']}."
            )
            return redirect("chat_app:user_list")
        else:
            messages.error(request, "Invalid Credentials...")
    return render(request, "accounts/login.html")


@login_required
def logout_view(request):
    """

        Log out the currently authenticated user.

        Updates the user's online status to offline, ends the user session,

        and redirects to the login page.

        Args:

        request (HttpRequest): The incoming HTTP request.

        Returns:

        HttpResponse: Redirects the user to the login page after logout.

        Side Effects:

        - Updates the user's online status.

        - Terminates the current user session.

    """
    request.user.is_online = False
    request.user.save()
    logout(request)
    return redirect("accounts:login")
