from django.contrib import admin
from gestion_documental.models.trd_models import (
    TablaRetencionDocumental,

    DisposicionFinalSeries,
    TipologiasDocumentales,
)
from gestion_documental.models.tca_models import (
    TablasControlAcceso,
    ClasificacionSeriesSubDoc,
    PermisosGD,
    CCD_Clasif_Cargos_UndCargo_Permisos
)

admin.site.register(TablaRetencionDocumental),
admin.site.register(DisposicionFinalSeries),
admin.site.register(TipologiasDocumentales),
admin.site.register(TablasControlAcceso),
admin.site.register(ClasificacionSeriesSubDoc),
admin.site.register(PermisosGD),
admin.site.register(CCD_Clasif_Cargos_UndCargo_Permisos),


