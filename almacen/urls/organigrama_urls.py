from django.urls import path
from almacen.views import organigrama_views as views

urlpatterns = [
    # UNIDADES ORGANIZACIONALES
    path('unidades/update/<str:pk>/',views.UpdateUnidades.as_view(),name='unidades-org-update'),
    path('unidades/create/', views.CreateUnidades.as_view(), name='unidades-org-create'),

    # NIVELES
    path('niveles/create/', views.CreateNiveles.as_view(), name='create-niveles'),
    path('niveles/update/<str:id_organigrama>/', views.UpdateNiveles.as_view(), name='update-niveles'),

    #ACTIVACION
    path('organigrama/activación/<str:pk>/',views.ActivarOrganigrama.as_view(),name='activacion'),
    path('organigrama/create/', views.CreateOrgChart.as_view(),name="crear-organigrama"),
    path('organigrama/get/', views.GetOrganigrama.as_view(), name='get-organigrama'),
    
]