from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatSession, Message
from account1.models import Avatar
from django.contrib.auth.models import User

@login_required
def chat_session(request, admin_id):
    admin = get_object_or_404(User, id=admin_id)
    chat_session, created = ChatSession.objects.get_or_create(user=request.user, admin=admin)
    messages = chat_session.messages.all()
    
    # Получение аватарок для всех отправителей сообщений
    avatars = {}
    for message in messages:
        try:
            avatar = Avatar.objects.get(user=message.sender)
            avatars[message.sender.id] = avatar.avatar.url if avatar.avatar else None
        except Avatar.DoesNotExist:
            avatars[message.sender.id] = None
    
    return render(request, 'chat/chat_session.html', {
        'chat_session': chat_session,
        'messages': messages,
        'avatars': avatars
    })

@login_required
def send_message(request, session_id):
    chat_session = get_object_or_404(ChatSession, id=session_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        Message.objects.create(chat_session=chat_session, sender=request.user, content=content)
    return redirect('chat_session', admin_id=chat_session.admin.id)