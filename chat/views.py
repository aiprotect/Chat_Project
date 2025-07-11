from django.shortcuts import render, redirect, reverse
from django.views import View

from accounts.models import User


class ChatView(View):
    def get(self, requests, room_id):
        if requests.user.is_authenticated:
            id = User.objects.get(id=room_id)
            context = {
                'session': id,
                'id': room_id,
                'user' : requests.user
            }
            return render(requests, 'chat/room_page.html', context)
        else:
            return redirect(reverse('login-name'))