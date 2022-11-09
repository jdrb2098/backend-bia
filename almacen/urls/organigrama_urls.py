from django.urls import path
from almacen.views import organigrama_views as views

urlpatterns = [
    # UNIDADES ORGANIZACIONALES
    path('unidades/update/<str:pk>/',views.UpdateUnidades.as_view(),name='unidades-org-update'),
    path('unidades/create/', views.CreateUnidades.as_view(), name='unidades-org-create'),
    path('unidades/get-list/', views.GetUnidades.as_view(), name='unidades-get-list'),

    # NIVELES
    path('niveles/get-list/', views.GetNiveles.as_view(), name='get-list-niveles'),
    path('niveles/create/', views.CreateNiveles.as_view(), name='create-niveles'),
    path('niveles/update/<str:id_organigrama>/', views.UpdateNiveles.as_view(), name='update-niveles'),

    #ACTIVACION
    path('activacion/<str:pk>/',views.ActivarOrganigrama.as_view(),name='activacion'),
    path('create/', views.CreateOrgChart.as_view(),name="crear-organigrama"),
    path('get/', views.GetOrganigrama.as_view(), name='get-organigrama'),
    
]