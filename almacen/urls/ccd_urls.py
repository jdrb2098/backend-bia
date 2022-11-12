from django.urls import path
from almacen.views import ccd_views as views
from almacen.views.ccd_views import CreateCuadroClasificacionDocumental

urlpatterns = [
    # Cuadros de Clasificación Documental
    path('create/', views.CreateCuadroClasificacionDocumental.as_view(),name='create-ccd'),
    path('get-list/', views.GetCuadroClasificacionDocumental.as_view(),name='get-list-ccd'),

    # SUBSERIES
    path('subseries/create/<str:id_ccd>/', views.CreateSubseriesDoc.as_view(), name='create-subseries-ccd'),
    path('subseries/get-by-id/<str:id_ccd>/', views.GetSubseries.as_view(),name='id-get-subseries-ccd'),
]
