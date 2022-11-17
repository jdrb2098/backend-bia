from django.urls import path
from almacen.views import organigrama_views as views

urlpatterns = [
    # UNIDADES ORGANIZACIONALES
    path('unidades/update/<str:pk>/',views.UpdateUnidades.as_view(),name='unidades-org-update'),
    path('unidades/get-list/', views.GetUnidades.as_view(), name='unidades-get-list'),
    path('unidades/get-sec-sub/<str:id_organigrama>/', views.GetSeccionSubsecciones.as_view(), name='unidades-get-sec-sub'),

    # NIVELES
    path('niveles/get-list/', views.GetNiveles.as_view(), name='get-list-niveles'),
    path('niveles/update/<str:id_organigrama>/', views.UpdateNiveles.as_view(), name='update-niveles'),

    #ORGANIGRAMA
    path('create/', views.CreateOrgChart.as_view(),name="crear-organigrama"),
    path('get/', views.GetOrganigrama.as_view(), name='get-organigrama'),
    path('get-terminados/', views.GetOrganigramasTerminados.as_view(), name='get-terminados-organigrama'),
    path('update/<str:id_organigrama>/', views.UpdateOrganigrama.as_view(), name='update-organigrama'),
    path('finalizar/<str:pk>/', views.FinalizarOrganigrama.as_view(), name='finalizar-organigrama'),
    
]