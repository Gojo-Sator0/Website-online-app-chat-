from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import *
from .forms import *
# Create your views here.


@login_required
def chats_view(request, chatroom_name='public_chat'):
    chat_group = get_object_or_404(ChatRoom, name=chatroom_name)
    chat_messages = chat_group.messages.all()[:50]
    form = ChatmessageCreateForm()
    user_chatrooms = request.user.chat_groups.all()

    other_user = None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404()
        for member in chat_group.members.all():
            if member != request.user:
                other_user = member
                break

    if request.htmx:
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.chat = chat_group
            message.save()
            context = {
                'message': message,
                'user': request.user,
            }
            return render(request, 'chat/includes/chat_message_p.html', context )
    
    context = {
        'chat_messages': chat_messages,
        'form': form,
        'other_user':other_user,
        'chatroom_name':chatroom_name,
        'user_chatrooms': user_chatrooms,
    }

    return render(request, 'chat/chat_user.html', context)

User = get_user_model()

@login_required
def get_or_create_chatroom(request, username):

    if request.user.username == username:
        return redirect('chat:chats')

    other_user = get_object_or_404(User, username=username)
    my_chatrooms = request.user.chat_groups.filter(is_private=True)

    chatroom = None

    for chat in my_chatrooms:
        if other_user in chat.members.all():
            chatroom = chat
            break  # Найден существующий чат, выходим из цикла

    if not chatroom:
        chatroom = ChatRoom.objects.create(is_private=True)
        chatroom.members.add(other_user, request.user)
        chatroom.save()

    return redirect('chat:chatroom', chatroom.name)

