from django.urls import path
from almacen.views import mantenimientos_views as views

urlpatterns = [
    path('programados/get-by-id/<str:pk>/',views.GetMantenimientosProgramadosById.as_view(),name='mantenimientos-programados-id-get'),
    path('programados/get-list/',views.GetMantenimientosProgramadosList.as_view(),name='mantenimientos-programados-get'),
    path('programados/get-five-list/',views.GetMantenimientosProgramadosFiveList.as_view(),name='mantenimientos-programados-five-get'),
    path('ejecutados/get-list/',views.GetMantenimientosEjecutadosList.as_view(),name='mantenimientos-ejecutados-get'),
    path('ejecutados/get-five-list/',views.GetMantenimientosEjecutadosFiveList.as_view(),name='mantenimientos-ejecutados-five-get'),
    path('ejecutados/get-by-id/<str:pk>/',views.GetMantenimientosEjecutadosById.as_view(),name='mantenimientos-ejecutados-id-get'),
]