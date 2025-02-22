from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import *
from .forms import *

@login_required
def chats_view(request, chatroom_name=None):
    user_chatrooms = request.user.chat_groups.all()

    # Если у пользователя нет чатов, показываем сообщение
    if not user_chatrooms.exists():
        return render(request, "chat/no_chats.html")

    # Если чат не указан, переадресуем в первый доступный
    if chatroom_name is None:
        return redirect("chat:chatroom", chatroom_name=user_chatrooms.first().name)

    # Получаем чат (без проверки участников)
    chat_group = get_object_or_404(ChatRoom, name=chatroom_name)

    # Проверка доступа
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404()  # Приватные чаты только для участников
    else:
        if request.user not in chat_group.members.all():
            chat_group.members.add(request.user)  # Автоматически добавляем в групповой чат

    chat_messages = chat_group.messages.all()[:50]
    form = ChatmessageCreateForm()

    other_user = None
    if chat_group.is_private:
        other_user = chat_group.members.exclude(id=request.user.id).first()

        # Обработка удаления чата (для приватных чатов оба пользователя могут удалить)
    if request.method == "POST" and "delete_chat" in request.POST:
        if chat_group.is_private and request.user in chat_group.members.all():
            chat_group.delete()  # Удаляем чат
            return redirect("chat:chats")  # Перенаправляем на страницу со списком чатов
        else:
            raise Http404()  # Если пользователь не участник, возвращаем 404

    # Если запрос выполнен с использованием HTMX (AJAX)
    if request.htmx:
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)  # Создаем сообщение, но не сохраняем его в базу данных
            message.sender = request.user  # Устанавливаем отправителя
            message.chat = chat_group  # Устанавливаем чат
            message.save()  # Сохраняем сообщение в базу данных
            context = {
                'message': message,
                'user': request.user,
            }
            # Возвращаем HTML-фрагмент с новым сообщением
            return render(request, 'chat/includes/chat_message_p.html', context)

    context = {
        "chat_messages": chat_messages,
        "form": form,
        "other_user": other_user,
        "chatroom_name": chatroom_name,
        "user_chatrooms": user_chatrooms,
        "chat_group": chat_group,
    }
    return render(request, "chat/chat_user.html", context)



# Получаем модель пользователя
User = get_user_model()

# Представление для получения или создания приватного чата
@login_required  
def get_or_create_chatroom(request, username):
    # Если пользователь пытается создать чат с самим собой, перенаправляем его
    if request.user.username == username:
        return redirect('chat:chats')

    # Получаем объект пользователя, с которым создается чат, или возвращаем 404
    other_user = get_object_or_404(User, username=username)

    # Получаем все приватные чаты текущего пользователя
    my_chatrooms = request.user.chat_groups.filter(is_private=True)

    chatroom = None

    # Проверяем, существует ли уже чат с этим пользователем
    for chat in my_chatrooms:
        if other_user in chat.members.all():
            chatroom = chat
            break  # Если чат найден, выходим из цикла

    # Если чат не найден, создаем новый
    if not chatroom:
        chatroom = ChatRoom.objects.create(is_private=True)
        chatroom.members.add(other_user, request.user)  # Добавляем участников
        chatroom.save()

    # Перенаправляем пользователя в созданный или найденный чат
    return redirect('chat:chatroom', chatroom.name)

@login_required
def create_groupchat(request):
    form = NewGroupForm()

    if request.method == 'POST':
        form = NewGroupForm(request.POST)
        if form.is_valid():
            groupchat = form.save(commit=False)
            groupchat.admin = request.user
            groupchat.save()
            groupchat.members.add(request.user)
            groupchat.save()
            return redirect('chat:chatroom', groupchat.name)

    context = {
        'form': form
    }
    return render(request, 'chat/create_groupchat.html', context)


@login_required
def chatroom_edit_view(request, chatroom_name):
    chat_group = get_object_or_404(ChatRoom, name=chatroom_name)

   
    
    form = ChatRoomEditForm(instance=chat_group)

    if request.method == "POST":
        # Удаление группы
        if "delete_chat" in request.POST:
            chat_group.delete()
            return redirect("chat:chats")  # Перенаправление на страницу со списком чатов

        # Обновление названия группы и удаление пользователей
        form = ChatRoomEditForm(request.POST, instance=chat_group)
        if form.is_valid():
            form.save()
            remove_members = request.POST.getlist('remove_members')
            for member_id in remove_members:
                member = User.objects.get(id=member_id)
                chat_group.members.remove(member)

            return redirect('chat:edit-group', chatroom_name)
    
    context = {
        "form": form,
        "chat_group": chat_group,
    }
    return render(request, "chat/edit_chatroom.html", context)

@login_required
def chatroom_leave_view(request, chatroom_name):
    chat_group = get_object_or_404(ChatRoom, name=chatroom_name)

    # Проверяем, что пользователь является участником чата
    if request.user in chat_group.members.all():
        chat_group.members.remove(request.user)  # Удаляем пользователя из участников
        chat_group.save()

    return redirect("chat:chats")  # Перенаправляем на страницу со списком чатов