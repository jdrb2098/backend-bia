from django.urls import path
from seguridad.views import user_views as views


urlpatterns = [
    
    path('login/', views.LoginApiView.as_view(), name='token_obtain_pair'),

    path('register/', views.RegisterView.as_view(), name='register'),
    
    path('profile/', views.getUserProfile, name="users-profile"),
    path('profile/update/', views.updateUserProfile, name="user-profile-update"), 
   
    path('roles/', views.roles, name='roles'),
    path("get/", views.getUsers, name="get-users"),
    path('email-varify/', views.VerifyEmail.as_view(), name='email-verify'),
    path("get/<str:pk>/", views.getUserById, name="get-users"), 
    
    
    #Login
    path('listarlogin/', views.LoginListApiViews.as_view(),name='mostrar-lista-login'),
    path('enviardatoslogin/', views.LoginRegisterApiViews.as_view(),name='enviar-datos-login'),
    path('consultarlogin/<int:pk>', views.LoginConsultarApiViews.as_view(),name='consultar-login'),
    path('eliminarlogin/<int:pk>', views.LoginDestroyApiViews.as_view(),name='actualizar-login'),
    path('actualizarlogin/<int:pk>', views.LoginUpdateApiViews.as_view(),name='eliminar-login'),
    #LoginErroneo
    path('listarloginerroneo/', views.LoginErroneoListApiViews.as_view(),name='mostrar-lista-login-erroneo'),
    path('enviardatosloginerroneo/', views.LoginErroneoRegisterApiViews.as_view(),name='enviar-datos-login-erroneo'),
    path('consultarloginerroneo/<int:pk>', views.LoginErroneoConsultarApiViews.as_view(),name='consultar-login-erroneo'),
    path('eliminarloginerroneo/<int:pk>', views.LoginErroneoDestroyApiViews.as_view(),name='actualizar-login-erroneo'),
    path('actualizarloginerroneo/<int:pk>', views.LoginErroneoUpdateApiViews.as_view(),name='eliminar-login-erroneo'),
    #UserRoles
    path('roles/register/', views.RegisterUserRoles.as_view(), name='user-rol-register'),
    path('roles/update/<int:pk>/', views.UpdateUserRoles.as_view(), name='user-rol-update'),
    path('roles/delete/<int:pk>/', views.DeleteUserRoles.as_view(), name='user-rol-delete')
]