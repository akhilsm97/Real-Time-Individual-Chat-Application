from django.urls import path

from . import views

app_name = "chat_app"
urlpatterns = [
    path("user_list/", views.user_list_view, name="user_list"),
    path("chat_view/<int:user_id>/", views.chat_view, name="chat_view"),
]
