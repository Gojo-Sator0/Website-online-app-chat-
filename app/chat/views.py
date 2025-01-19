from django.shortcuts import render
# Create your views here.

def chats_view(request):
    return render(request, 'chat/chat_user.html')


