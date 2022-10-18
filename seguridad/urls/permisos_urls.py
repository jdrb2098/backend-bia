from django.urls import path
from seguridad.views import permisos_views as views

app_name = 'permisos_app'

urlpatterns = [
    #Permisos
    path('update/<pk>/', views.UpdatePermiso.as_view(), name='permiso-update'),
    path('create/', views.InsertarPermiso.as_view(), name='permiso-insertar'),
    path('get-list/', views.ListarPermisos.as_view(), name='permiso-listar'),
    path('delete/<pk>/', views.DeletePermiso.as_view(), name='permiso-delete'),  
    path('get-by-id/<pk>/', views.DetailPermisos.as_view(), name='permiso-ver'),
    
    #Modulo
    path('modulos/get-list/', views.ListarModulo.as_view(),name='mostrar-lista-módulo'),
    path('modulos/create/', views.InsertarModulo.as_view(),name='enviar-datos-módulo'),
    path('modulos/get-by-id/<int:pk>', views.DetailModulo.as_view(),name='consultar-módulo'),
    path('modulos/delete/<int:pk>', views.DeleteModulo.as_view(),name='actualizar-módulo'),
    path('modulos/update/<int:pk>', views.UpdateModulo.as_view(),name='eliminar-módulo')
    
    #PermisosModulo
    #path('permisos-modulos/update/<pk>/', views.UpdatePermisoModulo.as_view(), name='permiso-update'),    
    #path('permisos-modulos/get-list/', views.ListarPermisosModulo.as_view(), name='permisos-modulo-listar'),
    #path('permisos-modulos/get-by-id/<str:pk>', views.DetailPermisosModulo.as_view(), name='permisos-modulo-ver'),
    #path('permisos-modulos/create/', views.InsertarPermisosModulo.as_view(), name='permiso-modulo-insertar'),
    #path('permisos-modulos/delete/<str:pk>/', views.DeletePermisosModulo.as_view(), name='permiso-modulo-delete'),  
    
    #PermisosModuloRol
    #path('permisos-modulos-rol/update/<pk>/', views.UpdatePermisoModuloRol.as_view(), name='permiso-modulo-rol-update'),    
    #path('permisos-modulos-rol/get-list/', views.ListarPermisosModuloRol.as_view(), name='permisos-modulo-rol-listar'),
    #path('permisos-modulos-rol/get-by-id/<pk>', views.DetailPermisosModuloRol.as_view(), name='permisos-modulo-rol-ver'),
    #path('permisos-modulos-rol/create/', views.InsertarPermisosModuloRol.as_view(), name='permiso-modulo-rol-insertar'),
    #path('permisos-modulos-rol/delete/<pk>/', views.DeletePermisosModuloRol.as_view(), name='permiso-modulo-rol-delete'),
]