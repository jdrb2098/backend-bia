from django.urls import path
from gestion_documental.views import trd_views as views

urlpatterns = [
    # TIPOLOGIAS DOCUMENTALES
    path('tipologias/create/<str:id_trd>/', views.CreateTipologiasDocumentales.as_view(), name='create-tipologias-doc'),
    path('tipologias/get-by-id/<str:id_trd>/', views.GetTipologiasDocumentales.as_view(),name='id-get-tipologias-doc'),
    
]