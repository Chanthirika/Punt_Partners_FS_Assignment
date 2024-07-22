
from django.urls import path
from .views import VoiceBot, HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),  # Serve the frontend
    path('voice/', VoiceBot.as_view(), name='voice_bot'),  # Backend for voice processing
]