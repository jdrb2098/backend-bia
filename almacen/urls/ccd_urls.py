from django.urls import path
from almacen.views import ccd_views as views
from almacen.views.ccd_views import CreateCuadroClasificacionDocumental

urlpatterns = [
    # Cuadros de Clasificación Documental
    path('create/', views.CreateCuadroClasificacionDocumental.as_view(),name='create-ccd'),
    path('get-list/', views.GetCuadroClasificacionDocumental.as_view(),name='get-list-ccd'),

    
]
