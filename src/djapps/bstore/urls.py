from django.urls import path

from .views import BlocksView, blocks_partial

app_name = 'bstore'

urlpatterns = [
    path('blocks/', BlocksView.as_view(), name='blocks'),
    path('blocks/detail/<int:block_id>/', BlocksView.as_view(), name='block_detail'),
    path('blocks/partial/', blocks_partial, name='blocks_partial'),
]
