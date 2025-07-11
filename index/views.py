from django.shortcuts import render
from django.views import View
from django.http import HttpRequest
from accounts.models import User

class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            context = {'session': request.user}
        else:
            context = {}

        return render(request, 'index/index_page.html', context=context)