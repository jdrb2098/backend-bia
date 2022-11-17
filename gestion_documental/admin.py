from django.contrib import admin
from gestion_documental.models.trd_models import (
    TablaRetencionDocumental,
    TiposSoportesDocumentos,
    FormatosTipoSoporte,
    DisposicionFinalSeries,
    TipologiasDocumentales,
    SeriesSubSeriesUnidadesTipologias,
    TablasControAcceso,
    ClasificacionSeriesSubDoc,
    PermisosGD,
    CCD_Clasif_Cargos_UndCargo_Permisos
)

admin.site.register(TablaRetencionDocumental),
admin.site.register(TiposSoportesDocumentos),
admin.site.register(FormatosTipoSoporte),
admin.site.register(DisposicionFinalSeries),
admin.site.register(TipologiasDocumentales),
admin.site.register(SeriesSubSeriesUnidadesTipologias),
admin.site.register(TablasControAcceso),
admin.site.register(ClasificacionSeriesSubDoc),
admin.site.register(PermisosGD),
admin.site.register(CCD_Clasif_Cargos_UndCargo_Permisos),


