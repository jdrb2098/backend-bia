from django.urls import path
from seguridad.views import personas_views as views


urlpatterns = [
    
    # Estado Civil 
    path('getestadoscivil/', views.getEstadoCivil, name="estado-civil-get"),
    path('getestadocivil/<str:pk>/', views.getEstadoCivilById, name='estado-civil-id-get'),
    path('deleteestadocivil/<str:pk>/', views.deleteEstadoCivil, name='estado-civil-delete'),
    path('updateestadocivil/<str:pk>/', views.updateEstadoCivil, name='estado-civil-update'),
    path('registerestadocivil/', views.registerEstadoCivil, name='estado-civil-register'),
    
    # Tipo Documento 
    path('gettiposdocumento/', views.getTipoDocumento, name="tipo-documento-get"),
    path('gettipodocumento/<str:pk>/', views.getTipoDocumentoById, name='tipo-documento-id-get'),
    path('deletetipodocumento/<str:pk>/', views.deleteTipoDocumento, name='tipo-documento-delete'),
    path('updatetipodocumento/<str:pk>/', views.updateTipoDocumento, name='tipo-documento-update'),
    path('registertipodocumento/', views.registerTipoDocumento, name='tipo-documento-register'),
    
    # Personas 
    path('getpersonas/', views.getPersonas, name="personas-get"),
    path('getpersona/<str:pk>/', views.getPersonaById, name='persona-id-get'),
    path('deletepersona/<str:pk>/', views.deletePersona, name='persona-delete'),
    path('updatepersona/<str:pk>/', views.UpdatePersona.as_view(), name='persona-update'),
    path('registerpersona/', views.RegisterPersona.as_view(), name='persona-register'),
    
    # Apoderados Personas
    path('getapoderadospersonas/', views.getApoderadosPersona, name="apoderados-personas-get"),
    path('getapoderadopersona/<str:pk>/', views.getApoderadoPersonaById, name='apoderado-persona-id-get'),
    path('deleteapoderadopersona/<str:pk>/', views.deleteApoderadoPersona, name='apoderado-persona-delete'),
    path('updateapoderadopersona/<str:pk>/', views.updateApoderadoPersona, name='apoderado-persona-update'),
    path('registerapoderadopersona/', views.registerApoderadoPersona, name='apoderado-persona-register'),
    
    # Sucursales Empresas
    path('getsucursalesempresas/', views.getSucursalesEmpresas, name="sucursales-empresas-get"),
    path('getsucursalempresa/<str:pk>/', views.getSucursalEmpresaById, name='sucursal-empresa-id-get'),
    path('deletesucursalempresa/<str:pk>/', views.deleteSucursalEmpresa, name='sucursal-empresa-delete'),
    path('updatesucursalempresa/<str:pk>/', views.updateSucursalEmpresa, name='sucursal-empresa-update'),
    path('registersucursalempresa/', views.registerSucursalEmpresa, name='sucursal-empresa-register'),
    
    # Historico Emails
    path('gethistoricoemails/', views.getHistoricoEmails, name="historico-emails-get"),
    path('gethistoricoemail/<str:pk>/', views.getHistoricoEmailById, name='historico-email-id-get'),
    path('deletehistoricoemail/<str:pk>/', views.deleteHistoricoEmail, name='historico-email-delete'),
    path('updatehistoricoemail/<str:pk>/', views.updateHistoricoEmail, name='historico-email-update'),
    path('registerhistoricoemail/', views.registerHistoricoEmail, name='historico-email-register'),
    
    # Historico Direcciones
    path('gethistoricodirecciones/', views.GetHistoricoDirecciones.as_view(), name="historico-direcciones-get"),
    path('gethistoricodireccion/<str:pk>/', views.GetHistoricoDireccionById.as_view(), name='historico-direccion-id-get'),
    path('deletehistoricodireccion/<str:pk>/', views.DeleteHistoricoDireccion.as_view(), name='historico-direccion-delete'),
    path('updatehistoricodireccion/<str:pk>/', views.UpdateHistoricoDireccion.as_view(), name='historico-direccion-update'),
    path('registerhistoricodireccion/', views.RegisterHistoricoDireccion.as_view(), name='historico-direccion-register'),
    
    # Clases Tercero
    path('getclasestercero/', views.getClasesTercero, name="clases-tercero-get"),
    path('getclasetercero/<str:pk>/', views.getClaseTerceroById, name='clase-tercero-id-get'),
    path('deleteclasetercero/<str:pk>/', views.deleteClaseTercero, name='clase-tercero-delete'),
    path('updateclasetercero/<str:pk>/', views.updateClaseTercero, name='clase-tercero-update'),
    path('registerclasetercero/', views.registerClaseTercero, name='clase-tercero-register'),
    
    # Clases Tercero
    path('getclasesterceropersonas/', views.getClasesTerceroPersonas, name="clases-tercero-personas-get"),
    path('getclaseterceropersona/<str:pk>/', views.getClaseTerceroPersonaById, name='clase-tercero-persona-id-get'),
    path('deleteclaseterceropersona/<str:pk>/', views.deleteClaseTerceroPersona, name='clase-tercero-persona-delete'),
    path('updateclaseterceropersona/<str:pk>/', views.updateClaseTerceroPersona, name='clase-tercero-persona-update'),
    path('registerclaseterceropersona/', views.registerClaseTerceroPersona, name='clase-tercero-persona-register'),

    path('paises/', views.PaisesChoices.as_view(), name='paises')

]