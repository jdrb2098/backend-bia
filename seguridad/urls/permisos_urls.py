from django.urls import path
from seguridad.views import permisos_views as views


urlpatterns = [
    path('update_permiso/<str:pk>/', views.updatePermiso, name='permiso-update'),
    path('insertar_permiso/', views.insertarPermiso, name='permiso-insertar'),
    path('ver_permiso/<str:pk>/', views.verPermiso, name='permiso-ver'),
    path('listar_permisos/', views.listarPermisos, name='permiso-listar'),
    path('delete_permiso/<str:pk>/', views.deletePermiso, name='permiso-delete'),  
    
    path('listar_permisos_modulo/', views.listarPermisosModulo, name='permisos-modulo-listar'),
    path('ver_permisos_modulo/<str:pk>', views.verPermisosModulo, name='permisos-modulo-ver'),
    path('insertar_permisos_modulo/', views.insertarPermisosModulo, name='permiso-modulo-insertar'),
    path('delete_permisos_modulo/<str:pk>/', views.deletePermisosModulo, name='permiso-modulo-delete'),  
    
    path('listar_permisos_modulo_rol/', views.listarPermisosModuloRol, name='permisos-modulo-rol-listar'),
    path('ver_permisos_modulo_rol/<str:pk>', views.verPermisosModuloRol, name='permisos-modulo-rol-ver'),
    path('insertar_permisos_modulo_rol/', views.insertarPermisosModuloRol, name='permiso-modulo-rol-insertar'),
    path('delete_permisos_modulo_rol/<str:pk>/', views.deletePermisosModuloRol, name='permiso-modulo-rol-delete'),  
]