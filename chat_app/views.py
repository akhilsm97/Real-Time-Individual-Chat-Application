from accounts.models import CustomUser
from chat_app.models import Message
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

# Create your views here.


@login_required
def user_list_view(request):
    """
    List/Display to all users but exclude the currently logged-in user.


    Accessible only to authenticated users (login_required protected view)
    fetch all users where the currently logged-in user is excluded from
    that list; renders them via the 'chat/user_list.html' template.


    Args:
        request (HttpRequest): the http request that was sent.


    Returns:
        HttpResponse: render the 'chat/user_list.html' template with context
        containing the list of users.


    Context:
        users (QuerySet[CustomUser]): a list of all users excluding the
        currently logged-in user.
    """
    users = CustomUser.objects.exclude(id=request.user.id)
    return render(request, "chat/user_list.html", {"users": users})


@login_required
def chat_view(request, user_id):
    """
    Show the chat conversation between the logged-in user and another user.


    This view retrieves all messages exchanged between the logged-in
    user and the specified user identified by `user_id` in timestamp
    order (oldest first). Additionally, it marks all unread messages from
    the other user as read.


    Parameters:
        request (HttpRequest): The HTTP request being sent.
        user_id (int): The identifier of the other user to chat with.


    Returns:
        HttpResponse: The `chat/chat.html` template rendered with the context
        containing the corresponding user as well as the message history.


    Context:
        other_user (CustomUser): The user being chatted with.
        messages (QuerySet[Message]): A list of messages exchanged
        between these two users.


    Side Effects:
        All unread messages sent by the `other_user` to the current user
        will be marked as read.
    """
    other_user = get_object_or_404(CustomUser, id=user_id)
    messages = Message.objects.filter(
        sender__in=[request.user, other_user], receiver__in=[request.user, other_user]
    ).order_by("timestamp")
    print("MY MESSAGES", messages)

    Message.objects.filter(
        sender=other_user, receiver=request.user, is_read=False
    ).update(is_read=True)

    return render(
        request, "chat/chat.html", {"other_user": other_user, "messages": messages}
    )
