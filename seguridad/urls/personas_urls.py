from django.urls import path
from seguridad.views import personas_views as views


urlpatterns = [
    
    # Estado Civil 
    path('getestadoscivil/', views.getEstadoCivil.as_view(), name="estado-civil-get"),
    path('getestadocivil/<str:pk>/', views.getEstadoCivilById.as_view(), name='estado-civil-id-get'),
    path('deleteestadocivil/<str:pk>/', views.deleteEstadoCivil.as_view(), name='estado-civil-delete'),
    path('updateestadocivil/<str:pk>/', views.updateEstadoCivil.as_view(), name='estado-civil-update'),
    path('registerestadocivil/', views.registerEstadoCivil.as_view(), name='estado-civil-register'),
    
    # Tipo Documento 
    path('gettiposdocumento/', views.getTipoDocumento.as_view(), name="tipo-documento-get"),
    path('gettipodocumento/<str:pk>/', views.getTipoDocumentoById.as_view(), name='tipo-documento-id-get'),
    path('deletetipodocumento/<str:pk>/', views.deleteTipoDocumento.as_view(), name='tipo-documento-delete'),
    path('updatetipodocumento/<str:pk>/', views.updateTipoDocumento.as_view(), name='tipo-documento-update'),
    #path('registertipodocumento/', views.registerTipoDocumento.as_view(), name='tipo-documento-register'),
    
    # Personas 
    path('getpersonas/', views.getPersonas.as_view(), name="personas-get"),
    path('getpersona/<str:pk>/', views.getPersonaById.as_view(), name='persona-id-get'),
    path('deletepersona/<str:pk>/', views.deletePersona.as_view(), name='persona-delete'),
    path('updatepersona/<str:pk>/', views.UpdatePersona.as_view(), name='persona-update'),
    path('registerpersona/', views.RegisterPersona.as_view(), name='persona-register'),
    path('getpersonabydocument/<str:pk>', views.getPersonaByDocument, name='persona-document-get'),
    path('getpersonabyemail/<str:pk>', views.getPersonaByEmail, name='persona-email-get'),
    
    # Apoderados Personas
    path('getapoderadospersonas/', views.getApoderadosPersona.as_view(), name="apoderados-personas-get"),
    path('getapoderadopersona/<str:pk>/', views.getApoderadoPersonaById.as_view(), name='apoderado-persona-id-get'),
    path('deleteapoderadopersona/<str:pk>/', views.deleteApoderadoPersona.as_view(), name='apoderado-persona-delete'),
    path('updateapoderadopersona/<str:pk>/', views.updateApoderadoPersona.as_view(), name='apoderado-persona-update'),
    path('registerapoderadopersona/', views.registerApoderadoPersona.as_view(), name='apoderado-persona-register'),
    
    # Sucursales Empresas
    path('getsucursalesempresas/', views.getSucursalesEmpresas.as_view(), name="sucursales-empresas-get"),
    path('getsucursalempresa/<str:pk>/', views.getSucursalEmpresaById.as_view(), name='sucursal-empresa-id-get'),
    path('deletesucursalempresa/<str:pk>/', views.deleteSucursalEmpresa.as_view(), name='sucursal-empresa-delete'),
    path('updatesucursalempresa/<str:pk>/', views.updateSucursalEmpresa.as_view(), name='sucursal-empresa-update'),
    path('registersucursalempresa/', views.registerSucursalEmpresa.as_view(), name='sucursal-empresa-register'),
    
    # Historico Emails
    path('gethistoricoemails/', views.getHistoricoEmails.as_view(), name="historico-emails-get"),
    path('gethistoricoemail/<str:pk>/', views.getHistoricoEmailById.as_view(), name='historico-email-id-get'),
    path('deletehistoricoemail/<str:pk>/', views.deleteHistoricoEmail.as_view(), name='historico-email-delete'),
    path('updatehistoricoemail/<str:pk>/', views.updateHistoricoEmail.as_view(), name='historico-email-update'),
    path('registerhistoricoemail/', views.registerHistoricoEmail.as_view(), name='historico-email-register'),
    
    # Historico Direcciones
    path('gethistoricodirecciones/', views.GetHistoricoDirecciones.as_view(), name="historico-direcciones-get"),
    path('gethistoricodireccion/<str:pk>/', views.GetHistoricoDireccionById.as_view(), name='historico-direccion-id-get'),
    path('deletehistoricodireccion/<str:pk>/', views.DeleteHistoricoDireccion.as_view(), name='historico-direccion-delete'),
    path('updatehistoricodireccion/<str:pk>/', views.UpdateHistoricoDireccion.as_view(), name='historico-direccion-update'),
    path('registerhistoricodireccion/', views.RegisterHistoricoDireccion.as_view(), name='historico-direccion-register'),
    
    # Clases Tercero
    path('getclasestercero/', views.getClasesTercero.as_view(), name="clases-tercero-get"),
    path('getclasetercero/<str:pk>/', views.getClaseTerceroById.as_view(), name='clase-tercero-id-get'),
    path('deleteclasetercero/<str:pk>/', views.deleteClaseTercero.as_view(), name='clase-tercero-delete'),
    path('updateclasetercero/<str:pk>/', views.updateClaseTercero.as_view(), name='clase-tercero-update'),
    path('registerclasetercero/', views.registerClaseTercero.as_view(), name='clase-tercero-register'),
    
    # Clases Tercero
    path('getclasesterceropersonas/', views.getClasesTerceroPersonas.as_view(), name="clases-tercero-personas-get"),
    path('getclaseterceropersona/<str:pk>/', views.getClaseTerceroPersonaById.as_view(), name='clase-tercero-persona-id-get'),
    path('deleteclaseterceropersona/<str:pk>/', views.deleteClaseTerceroPersona.as_view(), name='clase-tercero-persona-delete'),
    path('updateclaseterceropersona/<str:pk>/', views.updateClaseTerceroPersona.as_view(), name='clase-tercero-persona-update'),
    path('registerclaseterceropersona/', views.registerClaseTerceroPersona.as_view(), name='clase-tercero-persona-register'),

]