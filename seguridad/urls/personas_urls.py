from django.urls import path
from seguridad.views import personas_views as views


urlpatterns = [
    # Estado Civil
    path('registerestadocivil/', views.registerEstadoCivil, name='estado-civil-register'), 
    path('getestadocivil/', views.getEstadoCivil, name="estado-civil-get"),
    path('updateestadocivil/<str:pk>/', views.updateEstadoCivil, name='estado-civil-update'),
    path('deleteestadocivil/<str:pk>/', views.deleteEstadoCivil, name='estado-civil-delete'),
    path('getestadocivil/<str:pk>/', views.getEstadoCivilById, name='estado-civil-id-get'),

    # Tipo Documento
    path('registertipodocumento/', views.registerTipoDocumento, name='tipo-documento-register'), 
    path('gettipodocumento/', views.getTipoDocumento, name="tipo-documento-get"),
    path('gettipodocumento/<str:pk>/', views.getTipoDocumentoById, name='tipo-documento-id-get'),
    path('updatetipodocumento/<str:pk>/', views.updateTipoDocumento, name='tipo-documento-update'),
    path('deletetipodocumento/<str:pk>/', views.deleteTipoDocumento, name='tipo-documento-delete'),

]