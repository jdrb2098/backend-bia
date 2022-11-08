from django.contrib import admin
from almacen.models.organigrama_models import (
    Organigramas,
    NivelesOrganigrama,
    UnidadesOrganizacionales,
    Cargos
)

admin.site.register(Organigramas)
admin.site.register(NivelesOrganigrama)
admin.site.register(UnidadesOrganizacionales)
admin.site.register(Cargos)