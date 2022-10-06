from django.urls import path
from seguridad.views import user_views as views


urlpatterns = [
<<<<<<< HEAD
    path('login/', views.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),

    path('register/', views.registerUser, name='register'),

    path('profile/', views.getUserProfile, name="users-profile"),
    path('profile/update/', views.updateUserProfile, name="user-profile-update"),
    path('registerasd/', views.RegisterView.as_view(), name='register2'), 
=======
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # User
    
>>>>>>> 4acd03b5d9162e4f8f55a1c87cb01a5e6b031e45
    path('', views.getUsers, name="users"),
    path('<str:pk>/', views.getUserById, name='user'),
    path('delete/<str:pk>/', views.deleteUser, name='user-delete'),
    path('update/<str:pk>/', views.updateUser, name='user-update'),
<<<<<<< HEAD

    path('delete/<str:pk>/', views.deleteUser, name='user-delete'),
     
=======
    path('register/', views.registerUser, name='register'),
    path('profile/', views.getUserProfile, name="users-profile"),
    path('profile/update/', views.updateUserProfile, name="user-profile-update"), 
    
    # Roles
    path('roles/', views.roles, name='roles'), 
>>>>>>> 4acd03b5d9162e4f8f55a1c87cb01a5e6b031e45
]