from django.urls import path
from gestion_documental.views import trd_views as views

urlpatterns = [
    # TIPOLOGIAS DOCUMENTALES
    path('tipologias/update/<str:id_trd>/', views.UpdateTipologiasDocumentales.as_view(), name='update-tipologias-doc'),
    path('tipologias/get-by-id/<str:id_trd>/', views.GetTipologiasDocumentales.as_view(),name='id-get-tipologias-doc'),
    
    # TABLA DE RETENCION DOCUMENTAL
    path('get-terminados/', views.GetTablaRetencionDocumentalTerminados.as_view(), name='trd-terminados-get'),
    path('get-list/', views.GetTablaRetencionDocumental.as_view(), name='trd-get-list'),
    path('create/', views.PostTablaRetencionDocumental.as_view(), name='trd-create'),
    path('update/<str:pk>/', views.UpdateTablaRetencionDocumental.as_view(), name='trd-update'),
    path('finish/<str:id_trd>/', views.FinalizarTablaRetencionDocumental.as_view(), name='trd-finish'),
    path('activar/<str:pk>/',views.Activar.as_view(),name='activar')

]