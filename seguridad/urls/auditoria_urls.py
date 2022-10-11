from django.urls import path
from seguridad.views import auditorias_views as views

urlpatterns = [
    #Auditoria
    path('', views.ListApiViews.as_view(),name='mostrar-lista-auditoría'),
    path('enviardatosauditoria/', views.RegisterApiViews.as_view(),name='enviar-datos-auditoría'),
    path('consultarauditoria/<int:pk>', views.ConsultarApiViews.as_view(),name='consultar-auditoria'),
    path('eliminarauditoria/<int:pk>', views.DestroyApiViews.as_view(),name='actualizar-auditoria'),
    path('actualizarauditoria/<int:pk>', views.UpdateApiViews.as_view(),name='eliminar-auditoria'),
]