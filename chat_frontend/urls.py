from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat, name='chat'),  # URL for the chat view
    path('api/chat/', views.get_response, name='get_response'),  # URL for the chatbot response
     path('clear-history/', views.clear_history, name='clear_history')
]
