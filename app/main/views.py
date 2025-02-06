from django.shortcuts import redirect, render

# Create your views here.
def index_view(request):
    if request.user.is_authenticated:
        return redirect('chat:chats')
    return render(request, 'main/index.html')