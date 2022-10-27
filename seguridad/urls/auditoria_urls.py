from django.urls import path
from seguridad.views import auditorias_views as views

urlpatterns = [
    #Auditoria
    path('get-list/', views.ListApiViews.as_view(),name='mostrar-lista-auditoría'),
    path('create/', views.RegisterApiViews.as_view(),name='enviar-datos-auditoría'),
    path('get-by-query-params/', views.getAuditorias,name='consultar-auditoria'),
    path('delete/<int:pk>', views.DestroyApiViews.as_view(),name='actualizar-auditoria'),
    path('update/<int:pk>', views.UpdateApiViews.as_view(),name='eliminar-auditoria'),
]