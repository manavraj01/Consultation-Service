from rest_framework.pagination import  LimitOffsetPagination

class CustomPagination(LimitOffsetPagination):
    default_limit = 10  # Set default limit of records per page
    max_limit = 100  # Maximum number of records per page