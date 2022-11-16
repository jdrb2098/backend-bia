from django.urls import path
from gestion_documental.views import trd_views as views

urlpatterns = [
    # TIPOLOGIAS DOCUMENTALES
    path('create/tipologias-documentales/<str:id_trd>/', views.CreateTipologiasDocumentales.as_view(), name='tipologias-documentales-create')
    
]