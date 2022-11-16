from django.urls import path
from gestion_documental.views import trd_views as views

urlpatterns = [
    # TIPOLOGIAS DOCUMENTALES
    path('tipologias/create/<str:id_trd>/', views.CreateTipologiasDocumentales.as_view(), name='create-tipologias-doc'),
    path('tipologias/get-by-id/<str:id_trd>/', views.GetTipologiasDocumentales.as_view(),name='id-get-tipologias-doc'),
    
    # TABLA DE RETENCION DOCUMENTAL
    path('get-terminados/', views.GetTablaRetencionDocumentalTerminados.as_view(), name='trd-terminados-get'),
    path('get-list/', views.GetTablaRetencionDocumental.as_view(), name='trd-get-list'),
    path('create/', views.PostTablaRetencionDocumental.as_view(), name='trd-create'),
    path('update/<str:pk>/', views.UpdateTablaRetencionDocumental.as_view(), name='trd-update'),

]