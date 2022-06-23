from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='detail'),
    path('prueba', views.send_query_db, name='query'),
    path('decode', views.retrieve_image, name='query'),
]