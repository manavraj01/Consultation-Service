from django.urls import path
from .views import (
    MessageCreate,
    MessageList,
    MessageRetrieveUpdateDestroyAPI,
)

urlpatterns = [
   
    path('', MessageCreate.as_view(), name='create_message'),
    path('all/', MessageList.as_view(), name='list_message'),
    path('<int:pk>/', MessageRetrieveUpdateDestroyAPI.as_view(), name='retrieve_update_destroy_message'),
]
