from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializers
from django.contrib.auth import authenticate
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from paginator.paginations import CustomPagination


class CustomUserRegistrationView(viewsets.ModelViewSet):
    """
    API endpoint that allows registration and management of CustomUser instances.

    Features:
    - List all users (GET request)
    - Retrieve a single user (GET request with ID)
    - Create a new user (POST request)
    - Update user details (PUT/PATCH requests)
    - Delete a user (DELETE request)

    Permissions:
    - AllowAny: Anyone can access this endpoint (no authentication required).

    Pagination:
    - Uses CustomPagination to limit results per page.

    Serializer:
    - Uses CustomUserSerializers to validate and serialize user data.
    """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializers
    permission_classes = [AllowAny]
    pagination_class = CustomPagination


class LoginView(APIView):
    """
    Implement JWT based authentication
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Post method to collect the username and password from users.
        """
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"status": "error", "message": "Username and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(
            request, username=username, password=password, is_active=True
        )

        if user is None:
            return Response(
                {"status": "error", "message": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)

        response = Response(
            {
                "status": "success",
                "message": "Login successful",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            },
            status=status.HTTP_200_OK,
        )

        #  Store refresh token in HTTPOnly cookie
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=60 * 60 * 24,  # 1 day
        )

        return response


class CookieTokenRefreshView(TokenRefreshView):
    """
    Refresh JWT access tokens using a refresh token stored in cookies.

    This view overrides the default TokenRefreshView to automatically
    retrieve the 'refresh_token' from the request cookies instead of
    expecting it in the request body.

    HTTP Method:
    - POST: Refresh the access token.

    Cookies:
    - 'refresh_token': The refresh token used to obtain a new access token.

    Returns:
    - 200 OK with the new access token if successful.
    - 401 Unauthorized if the refresh token is invalid or missing.
    """

    def post(self, request, *args, **kwargs):
        request.data["refresh"] = request.COOKIES.get("refresh_token")
        return super().post(request, *args, **kwargs)


class LogoutView(APIView):
    """
    Log out a user by blacklisting their refresh token and deleting the cookie.

    This view performs the following steps:
    1. Retrieves the 'refresh_token' from cookies.
    2. Blacklists the refresh token (if present) to prevent further use.
    3. Deletes the 'refresh_token' cookie from the client.
    4. Returns a confirmation message.

    HTTP Method:
    - POST: Log out the user.

    Cookies:
    - 'refresh_token': The refresh token to blacklist and remove.

    Returns:
    - 200 OK with message "Logged out".
    """

    def post(self, request):
        refresh = request.COOKIES.get("refresh_token")

        if refresh:
            token = RefreshToken(refresh)
            token.blacklist()

        response = Response({"message": "Logged out"})
        response.delete_cookie("refresh_token")
        return response
