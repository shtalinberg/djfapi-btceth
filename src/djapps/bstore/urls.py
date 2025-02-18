from django.urls import path

from .views import BlocksView, block_detail

app_name = 'bstore'

urlpatterns = [
    path('blocks/', BlocksView.as_view(), name='blocks'),
    path('blocks/detail/<int:block_id>/', block_detail, name='block_detail'),
]
