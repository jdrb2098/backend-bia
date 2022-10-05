from django.urls import path
from seguridad.views import auditorias_views as views

urlpatterns = [
    path('', views.mostrarListaAuditoria,name='mostrar-lista-auditoría'),
    path('enviarDatosAuditoria/', views.enviarDatosAuditoria,name='enviar-datos-auditoría'),
    path('consultarAuditoria/<int:pk>', views.consultarAuditoria,name='consultar-auditoria'),
    path('eliminarAuditoria/<int:pk>', views.eliminarAuditoria,name='actualizar-auditoria'),
    path('actualizarAuditoria/<int:pk>', views.actualizarAuditoria,name='eliminar-auditoria'),
    path('mostrarListaModulo/', views.mostrarListaModulo,name='mostrar-lista-módulo'),
    path('enviarDatosModulo/', views.enviarDatosModulo,name='enviar-datos-módulo'),
    path('consultarModulo/<int:pk>', views.consultarModulos,name='consultar-módulo'),
    path('eliminarModulo/<int:pk>', views.eliminarModulo,name='actualizar-módulo'),
    path('actualizarModulo/<int:pk>', views.actualizarModulo,name='eliminar-módulo')
]