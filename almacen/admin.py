from django.contrib import admin
from almacen.models.organigrama_models import (
    Organigramas,
    NivelesOrganigrama,
    UnidadesOrganizacionales,
    Cargos
)
from almacen.models.ccd_models import (
    CuadrosClasificacionDocumental,
    SubseriesDoc,
    SeriesDoc,
    SeriesSubseriesUnidadOrg
)
from almacen.models.generics_models import (
    Marcas,
    PorcentajesIVA,
    UnidadesMedida,
    Bodegas
)

admin.site.register(Organigramas)
admin.site.register(NivelesOrganigrama)
admin.site.register(UnidadesOrganizacionales)
admin.site.register(Cargos)
admin.site.register(Marcas)
admin.site.register(PorcentajesIVA)
admin.site.register(UnidadesMedida)
admin.site.register(Bodegas)
admin.site.register(CuadrosClasificacionDocumental)
admin.site.register(SubseriesDoc)
admin.site.register(SeriesDoc)
admin.site.register(SeriesSubseriesUnidadOrg)