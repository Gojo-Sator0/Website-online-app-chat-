from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
# Create your views here.

@login_required
def chats_view(request):
    chat_group = get_object_or_404(ChatRoom, name='public_chat')
    chat_messages = chat_group.messages.all()[:50]
    form = ChatmessageCreateForm()

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
        
    return render(request, 'chat/chat_user.html', {'chat_messages': chat_messages, 'form': form,} )


