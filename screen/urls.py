from django.contrib import admin
from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='host_scrn'),
    path('stop_screen/', views.stop_screen, name='stop_scrn'),
    path('start_screen/', views.start_screen, name='start_scrn'),
    path('end_stream/', views.end_stream, name='end_stream'),
    path('stream_scrn/', views.stream_screen, name='stream_scrn'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
