from django.urls import path
from seguridad.views import user_views as views


urlpatterns = [
    
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('register/', views.RegisterView.as_view(), name='register'),

    path('profile/', views.getUserProfile, name="users-profile"),
    path('profile/update/', views.updateUserProfile, name="user-profile-update"), 
   
    path('roles/', views.roles, name='roles'),
    path("", views.getUsers, name="get-users"),
    path("<str:pk>/", views.getUserById, name="get-users"), 
   
    path('roles/register/', views.RegisterUserRoles.as_view(), name='user-rol-register'),
    path('roles/update/<int:pk>/', views.UpdateUserRoles.as_view(), name='user-rol-update'),
    path('roles/delete/<int:pk>/', views.DeleteUserRoles.as_view(), name='user-rol-delete'),
]