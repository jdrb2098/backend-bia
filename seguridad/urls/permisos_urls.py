from django.urls import path
from seguridad.views import permisos_views as views

app_name = 'permisos_app'

urlpatterns = [
    path('update_permisos/<pk>/', views.UpdatePermiso.as_view(), name='permiso-update'),
    path('insertar_permisos/', views.InsertarPermiso.as_view(), name='permiso-insertar'),
    path('listar_permisos/', views.ListarPermisos.as_view(), name='permiso-listar'),
    path('delete_permisos/<pk>/', views.DeletePermiso.as_view(), name='permiso-delete'),  
    path('detail_permisos/<pk>/', views.DetailPermisos.as_view(), name='permiso-ver'),
        
    path('update_permisos_modulo/<pk>/', views.UpdatePermisoModulo.as_view(), name='permiso-update'),    
    path('listar_permisos_modulo/', views.ListarPermisosModulo.as_view(), name='permisos-modulo-listar'),
    path('detail_permisos_modulo/<str:pk>', views.DetailPermisosModulo.as_view(), name='permisos-modulo-ver'),
    path('insertar_permisos_modulo/', views.InsertarPermisosModulo.as_view(), name='permiso-modulo-insertar'),
    path('delete_permisos_modulo/<str:pk>/', views.DeletePermisosModulo.as_view(), name='permiso-modulo-delete'),  
    
    path('update_permisos_modulo_rol/<pk>/', views.UpdatePermisoModuloRol.as_view(), name='permiso-modulo-rol-update'),    
    path('listar_permisos_modulo_rol/', views.ListarPermisosModuloRol.as_view(), name='permisos-modulo-rol-listar'),
    path('detail_permisos_modulo_rol/<pk>', views.DetailPermisosModuloRol.as_view(), name='permisos-modulo-rol-ver'),
    path('insertar_permisos_modulo_rol/', views.InsertarPermisosModuloRol.as_view(), name='permiso-modulo-rol-insertar'),
    path('delete_permisos_modulo_rol/<pk>/', views.DeletePermisosModuloRol.as_view(), name='permiso-modulo-rol-delete'),  
      
    path('listar2_permisos_modulo_rol/', views.ListarPermisosModuloRol.as_view(), name='permiso-modulo-rol-listar-2'),
]