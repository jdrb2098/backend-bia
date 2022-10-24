from django.urls import path
from seguridad.views import personas_views as views


urlpatterns = [
    
    # Estado Civil 
    path('estado-civil/get-list/', views.getEstadoCivil.as_view(), name="estado-civil-get"),
    path('estado-civil/get-by-id/<str:pk>/', views.getEstadoCivilById.as_view(), name='estado-civil-id-get'),
    path('estado-civil/delete/<str:pk>/', views.deleteEstadoCivil.as_view(), name='estado-civil-delete'),
    path('estado-civil/create/', views.registerEstadoCivil.as_view(), name='estado-civil-register'),
    
    # Tipo Documento 
    path('tipos-documento/get-list/', views.getTipoDocumento.as_view(), name="tipo-documento-get"),
    path('tipos-documento/get-by-id/<str:pk>/', views.getTipoDocumentoById.as_view(), name='tipo-documento-id-get'),
    path('tipos-documento/delete/<str:pk>/', views.deleteTipoDocumento.as_view(), name='tipo-documento-delete'),
    path('tipos-documento/create/', views.registerTipoDocumento.as_view(), name='tipo-documento-register'),
    
    # Personas 
    path('get-list/', views.getPersonas.as_view(), name="personas-get"),
    path('get-by-email/<str:pk>/', views.getPersonaByEmail, name='persona-email-get'),
    path('get-personas-by-document/<str:tipodocumento>/<str:numerodocumento>/', views.GetPersonasByTipoDocumentoAndNumeroDocumento.as_view(), name='persona-by-document-and-tipo-documento-get'),
    path('get-personas-naturales-by-document/<str:tipodocumento>/<str:numerodocumento>/', views.GetPersonaNaturalByTipoDocumentoAndNumeroDocumento.as_view(), name='persona-natural-by-document-and-tipo-documento-get'),
    path('get-personas-juridicas-by-document/<str:tipodocumento>/<str:numerodocumento>/', views.GetPersonaJuridicaByTipoDocumentoAndNumeroDocumento.as_view(), name='persona-juridica-by-document-and-tipo-documento-get'),
    path('get-personas-naturales/', views.GetPersonaNatural.as_view(), name='persona-natural-get'),
    path('get-personas-juridicas/', views.GetPersonaJuridica.as_view(), name='persona-juridica-get'),
    path('persona-natural/update/<str:pk>/', views.UpdatePersonaNatural.as_view(), name='persona-natural-update'),
    path('persona-natural/create/', views.RegisterPersonaNatural.as_view(), name='persona-natural-register'),
    path('persona-juridica/create/', views.RegisterPersonaJuridica.as_view(), name='persona-juridica-register'),
    path('persona-juridica/update/<str:pk>/', views.UpdatePersonaJuridica.as_view(), name='persona-juridica-update'),
    path('delete/<str:pk>/', views.deletePersona.as_view(), name='persona-delete'),
    
    # Apoderados Personas
    path('apoderados-personas/get-list/', views.getApoderadosPersona.as_view(), name="apoderados-personas-get"),
    path('apoderados-personas/get-by-id/<str:pk>/', views.getApoderadoPersonaById.as_view(), name='apoderado-persona-id-get'),
    path('apoderados-personas/delete/<str:pk>/', views.deleteApoderadoPersona.as_view(), name='apoderado-persona-delete'),
    path('apoderados-personas/update/<str:pk>/', views.updateApoderadoPersona.as_view(), name='apoderado-persona-update'),
    path('apoderados-personas/create/', views.registerApoderadoPersona.as_view(), name='apoderado-persona-register'),
    
    # Sucursales Empresas
    path('sucursales-empresas/get-list/', views.getSucursalesEmpresas.as_view(), name="sucursales-empresas-get"),
    path('sucursales-empresas/get-by-id/<str:pk>/', views.getSucursalEmpresaById.as_view(), name='sucursal-empresa-id-get'),
    path('sucursales-empresas/delete/<str:pk>/', views.deleteSucursalEmpresa.as_view(), name='sucursal-empresa-delete'),
    path('sucursales-empresas/update/<str:pk>/', views.updateSucursalEmpresa.as_view(), name='sucursal-empresa-update'),
    path('sucursales-empresas/create/', views.registerSucursalEmpresa.as_view(), name='sucursal-empresa-register'),
    
    # Historico Emails
    # path('historico-emails/get-list/', views.getHistoricoEmails.as_view(), name="historico-emails-get"),
    # path('historico-emails/get-by-id/<str:pk>/', views.getHistoricoEmailById.as_view(), name='historico-email-id-get'),
    # path('historico-emails/delete/<str:pk>/', views.deleteHistoricoEmail.as_view(), name='historico-email-delete'),
    # path('historico-emails/update/<str:pk>/', views.updateHistoricoEmail.as_view(), name='historico-email-update'),
    # path('historico-emails/create/', views.registerHistoricoEmail.as_view(), name='historico-email-register'),
    
    # Historico Direcciones
    # path('historico-direcciones/get-list/', views.GetHistoricoDirecciones.as_view(), name="historico-direcciones-get"),
    # path('historico-direcciones/get-by-id/<str:pk>/', views.GetHistoricoDireccionById.as_view(), name='historico-direccion-id-get'),
    # path('historico-direcciones/delete/<str:pk>/', views.DeleteHistoricoDireccion.as_view(), name='historico-direccion-delete'),
    # path('historico-direcciones/update/<str:pk>/', views.UpdateHistoricoDireccion.as_view(), name='historico-direccion-update'),
    # path('historico-direcciones/create/', views.RegisterHistoricoDireccion.as_view(), name='historico-direccion-register'),
    
    # Clases Tercero
    # path('clases-tercero/get-list/', views.getClasesTercero.as_view(), name="clases-tercero-get"),
    # path('clases-tercero/get-by-id/<str:pk>/', views.getClaseTerceroById.as_view(), name='clase-tercero-id-get'),
    # path('clases-tercero/delete/<str:pk>/', views.deleteClaseTercero.as_view(), name='clase-tercero-delete'),
    # path('clases-tercero/update/<str:pk>/', views.updateClaseTercero.as_view(), name='clase-tercero-update'),
    # path('clases-tercero/create/', views.registerClaseTercero.as_view(), name='clase-tercero-register'),
    
    # Clases Tercero Personas
    # path('clases-tercero-personas/get-list/', views.getClasesTerceroPersonas.as_view(), name="clases-tercero-personas-get"),
    # path('clases-tercero-personas/get-by-id/<str:pk>/', views.getClaseTerceroPersonaById.as_view(), name='clase-tercero-persona-id-get'),
    # path('clases-tercero-personas/delete/<str:pk>/', views.deleteClaseTerceroPersona.as_view(), name='clase-tercero-persona-delete'),
    # path('clases-tercero-personas/update/<str:pk>/', views.updateClaseTerceroPersona.as_view(), name='clase-tercero-persona-update'),
    # path('clases-tercero-personas/create/', views.registerClaseTerceroPersona.as_view(), name='clase-tercero-persona-register'),

]