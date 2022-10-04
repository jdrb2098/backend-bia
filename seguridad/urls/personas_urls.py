from django.urls import path
from seguridad.views import personas_views as views


urlpatterns = [
    path('registerestadocivil', views.registerEstadoCivil, name='estado-civil-register'), 
    path('getestadocivil', views.getEstadoCivil, name="estado-civil-get"),
    path('updateestadocivil/<str:pk>/', views.updateEstadoCivil, name='estado-civil-update'),
    path('deleteestadocivil/<str:pk>/', views.deleteEstadoCivil, name='estado-civil-delete'),
    path('getestadocivil/<str:pk>/', views.getEstadoCivilById, name='estado-civil-id-get'),


]