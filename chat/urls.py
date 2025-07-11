from django.urls import path
from . import views

urlpatterns = [
    path('<uuid:room_id>/', views.ChatView.as_view(), name='chat-name'),
]