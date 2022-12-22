

from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns=[
  path('auth/', obtain_auth_token),
  path('api/post/', views.post_create_list, name = "list_product"),
  path('api/deletePost/<int:pk>/', views.post_retrieve_delete_update, name = "delete_post"),
  path('api/retrievePost/<int:pk>/', views.post_retrieve_delete_update, name = "retrieve_post"),
  path('api/updatePost/<int:pk>/', views.post_retrieve_delete_update, name = "update_post"),
  path('api/signup/', views.user_create, name="create_new_user"),
  path('api/login/', views.user_login, name="login_existing_user" ),
  path('api/logout/', views.user_logout, name = "logout_existing_user")
  
  
]