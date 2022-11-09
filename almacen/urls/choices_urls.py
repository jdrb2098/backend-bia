from django.urls import path
from almacen.views import choices_views as views

urlpatterns = [
    # Choices
    path('agrupacion-documental/', views.AgrupacionDocumentalChoices.as_view(), name='agrupacion-documental'),
    path('tipo-unidad/', views.TipoUnidadChoices.as_view(), name='tipo-unidad'),
    path('estados-articulo/', views.EstadosArticuloChoices.as_view(), name='estados-articulo'),
    path('magnitudes/', views.MagnitudesChoices.as_view(), name='magnitudes'),
]