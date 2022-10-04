from django.urls import path
from seguridad.views import permisos_views as views


urlpatterns = [
    path('update_permiso/<str:pk>/', views.updatePermiso, name='permiso-update'),
    path('insertar_permiso/', views.verPermiso, name='permiso-insertar'),
    path('ver_permiso/<str:pk>/', views.verPermiso, name='permiso-ver'),
    path('listar_permisos/', views.listarPermisos, name='permiso-listar'),
    path('delete_permiso/<str:pk>/', views.deletePermiso, name='permiso-delete'),  
]