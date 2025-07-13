from django.shortcuts import render, redirect, reverse
from django.views import View
from django.http import JsonResponse
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


def search_users(request):
    query = request.GET.get('q', '').strip()

    if not query or len(query) < 2:
        return JsonResponse({'results': []})

    users = User.objects.filter(
        username__icontains=query
    ).exclude(
        id=request.user.id  # کاربر جاری را از نتایج حذف می‌کند
    ).values('id', 'username')[:10]  # محدودیت ۱۰ نتیجه

    return JsonResponse({'results': list(users)})