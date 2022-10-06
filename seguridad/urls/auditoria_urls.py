from django.urls import path
from seguridad.views import auditorias_views as views

urlpatterns = [
    #Auditoria
    path('', views.mostrarListaAuditoria,name='mostrar-lista-auditoría'),
    path('enviardatosauditoria/', views.enviarDatosAuditoria,name='enviar-datos-auditoría'),
    path('consultarauditoria/<int:pk>', views.consultarAuditoria,name='consultar-auditoria'),
    path('eliminarauditoria/<int:pk>', views.eliminarAuditoria,name='actualizar-auditoria'),
    path('actualizarauditoria/<int:pk>', views.actualizarAuditoria,name='eliminar-auditoria'),
    #Modulo
    path('mostrarlistamodulo/', views.mostrarListaModulo,name='mostrar-lista-módulo'),
    path('enviardatosmodulo/', views.enviarDatosModulo,name='enviar-datos-módulo'),
    path('consultarmodulo/<int:pk>', views.consultarModulos,name='consultar-módulo'),
    path('eliminarmodulo/<int:pk>', views.eliminarModulo,name='actualizar-módulo'),
    path('actualizarmodulo/<int:pk>', views.actualizarModulo,name='eliminar-módulo')
]