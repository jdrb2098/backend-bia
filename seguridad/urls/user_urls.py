from django.urls import path
from seguridad.views import user_views as views


urlpatterns = [
    
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('register/', views.RegisterView.as_view(), name='register'),
    
    path('profile/', views.getUserProfile, name="users-profile"),
    path('profile/update/', views.updateUserProfile, name="user-profile-update"), 
   
    path('roles/', views.roles, name='roles'),
    path("get/", views.getUsers, name="get-users"),
    path('email-varify/', views.VerifyEmail.as_view(), name='email-verify'),
    path("get/<str:pk>/", views.getUserById, name="get-users"), 
    

    path("", views.getUsers, name="get-users"),
    path("<str:pk>/", views.getUserById, name="get-users"), 
    
   

]