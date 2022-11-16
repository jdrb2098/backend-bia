from django.urls import path
from almacen.views import ccd_views as views

urlpatterns = [
    # Cuadros de Clasificación Documental
    path('update/<str:pk>/', views.UpdateCuadroClasificacionDocumental.as_view(),name='update-ccd'),
    path('get-list/', views.GetCuadroClasificacionDocumental.as_view(),name='get-list-ccd'),
    path('get-terminados/', views.GetCCDTerminado.as_view(),name='get-terminados-ccd'),
    path('finish/<str:pk>/', views.FinalizarCuadroClasificacionDocumental.as_view(),name='finish-ccd'),
    path('resume/<str:pk>/', views.ReanudarCuadroClasificacionDocumental.as_view(),name='resume-ccd'),

    # SUBSERIES
    path('subseries/create/<str:id_ccd>/', views.CreateSubseriesDoc.as_view(), name='create-subseries-ccd'),
    path('subseries/get-by-id/<str:id_ccd>/', views.GetSubseries.as_view(),name='id-get-subseries-ccd'),

    # Series
    path('series/create/<str:id_ccd>/',views.CreateSeriesDoc.as_view(),name='crear-series-documentales'),
    path('series/get/<str:id_ccd>/',views.GetSeriesDoc.as_view(),name='get-series-documentales'),
    
    # Asignaciones
    path('asignar/create/<str:id_ccd>/',views.AsignarSeriesYSubseriesAUnidades.as_view(),name='asignar-series-documentales'),
    path('asignar/get//<str:id_ccd>/',views.GetAsignaciones.as_view(),name='asignar-series-documentales')
]
