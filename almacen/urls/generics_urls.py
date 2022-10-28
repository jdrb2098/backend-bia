from django.urls import path
from almacen.views import generics_views as views

urlpatterns = [
    
    #MARCAS
    path('marcas/create/',views.RegisterMarca.as_view(),name='marcas-create'),
    path('marcas/update/<pk>/',views.UpdateMarca.as_view(),name='marcas-update'),
    path('marcas/delete/<str:pk>/',views.DeleteMarca.as_view(), name='marcas-delete'),
    path('marcas/get-by-id/<str:pk>/',views.GetMarcaById.as_view(),name='marcas-id-get'),
    path('marcas/get-list/',views.GetMarcaList.as_view(),name='marcas-get'),

    # ESTADOS ARTICULO
    path('estados-articulo/get-by-id/<str:pk>/',views.GetEstadosArticuloById.as_view(),name='estados-articulo-id-get'),
    path('estados-articulo/get-list/',views.GetEstadosArticuloList.as_view(),name='estados-articulo-get'),
    
    #BODEGAS
    
    path('bodega/create/',views.RegisterBodega.as_view(),name='bodega-create'),
    path('bodega/update/<pk>/',views.UpdateBodega.as_view(),name='bodega-update'),
    path('bodega/delete/<str:pk>/',views.DeleteBodega.as_view(), name='bodega-delete'),
    path('bodega/get-by-id/<str:pk>/',views.GetBodegaById.as_view(),name='bodega-id-get'),
    path('bodega/get-list/',views.GetBodegaList.as_view(),name='bodega-get'),
]