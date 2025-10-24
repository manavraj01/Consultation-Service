from django.urls import path
from .views import (
    ConsultationCreate,
    ConsultationList,
    ConsultationRetrieveUpdateDestroyAPI,
)

urlpatterns = [
   
    path('', ConsultationCreate.as_view(), name='create_consultation'),

   
    path('all/', ConsultationList.as_view(), name='list_consultation'),

  
    path('<int:pk>/', ConsultationRetrieveUpdateDestroyAPI.as_view(), name='retrieve_update_destroy_consultation'),
]
