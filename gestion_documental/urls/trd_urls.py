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
    # path('finish/<str:id_trd>/', views.FinalizarTablaRetencionDocumental.as_view(), name='trd-finish'),
    path('activar/<str:pk>/',views.Activar.as_view(),name='activar'),

    # FORMATOS TIPOS MEDIO
    path('formatos/get-by-params/', views.GetFormatosTiposMedioByParams.as_view(), name='formatos-get-by-params'),
    path('formatos/get-by-cod/<str:cod_tipo_medio_doc>/', views.GetFormatosTiposMedioByCodTipoMedio.as_view(), name='formatos-get-by-cod'),
    path('formatos/create/', views.RegisterFormatosTiposMedio.as_view(), name='formatos-create'),
    path('formatos/update/<str:pk>/', views.UpdateFormatosTiposMedio.as_view(), name='formatos-update'),
    path('formatos/delete/<str:pk>/', views.DeleteFormatosTiposMedio.as_view(), name='formatos-delete')
]