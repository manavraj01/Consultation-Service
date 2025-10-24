from django.urls import path
from .views import (
    RoleCreate,
    RoleList,
    RoleRetrieveUpdateDestroyAPI
)

urlpatterns = [
     path('',RoleCreate.as_view(),name = 'create_role'),
     path('all/',RoleList.as_view(),name = 'list_role'),
     path('<int:pk>/',RoleRetrieveUpdateDestroyAPI.as_view(),name = 'retrieve_update_destroy_role')
]
