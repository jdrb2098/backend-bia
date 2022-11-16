from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from gestion_documental.serializers.trd_serializers import (
    TipologiasDocumentalesSerializer,
)
from almacen.models.ccd_models import (
    SeriesSubseriesUnidadOrg
)
from gestion_documental.models.trd_models import (
    TablaRetencionDocumental,
    SeriesSubSeriesUnidadesTipologias,
    TipologiasDocumentales
)

class CreateTipologiasDocumentales(generics.CreateAPIView):
    serializer_class = TipologiasDocumentalesSerializer
    queryset = TipologiasDocumentales.objects.all()
    
    def post(self, request, id_trd):
        data = request.data
        tipologias = TipologiasDocumentales.objects.filter(id_trd=id_trd)
        print("TIPOLOGIAS: ", tipologias)
        trd = TablaRetencionDocumental.objects.filter(id_trd=id_trd).first()
        if trd:
            if not trd.fecha_terminado:
                if data:
                    # VALIDAR QUE EL ID_TRD SEA EL MISMO
                    trd_list = [tipologia['id_trd'] for tipologia in data]
                    print("TRD_LIST: ", trd_list)
                    if len(set(trd_list)) != 1:
                        return Response({'success':False, 'detail':'Debe validar que las tipologias pertenezcan a un mismo TRD'}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        if trd_list[0] != int(id_trd):
                            return Response({'success':False, 'detail':'El id trd de la petición debe ser igual al enviado en url'}, status=status.HTTP_400_BAD_REQUEST)
                                     
                    # VALIDAR QUE LOS CODIGOS SEAN UNICOS
                    codigos_list = [tipologia['codigo'] for tipologia in data]
                    if len(codigos_list) != len(set(codigos_list)):
                        return Response({'success':False, 'detail':'Debe validar que los códigos de las tipologias sean únicos'}, status=status.HTTP_400_BAD_REQUEST)
                    
                    # VALIDAR QUE LOS NOMBRES SEAN UNICOS
                    nombres_list = [tipologia['nombre'] for tipologia in data]
                    if len(nombres_list) != len(set(nombres_list)):
                        return Response({'success':False, 'detail':'Debe validar que los nombres de las tipologias sean únicos'}, status=status.HTTP_400_BAD_REQUEST)
                    
                    # CREAR TIPOLOGIAS
                    tipologias_create = list(filter(lambda tipologia: tipologia['id_tipologia_documental'] == None, data))
                    tipologias_id_create = []
                    if tipologias_create:
                        serializer = self.serializer_class(data=tipologias_create, many=True)
                        serializer.is_valid(raise_exception=True)
                        serializador = serializer.save()
                        tipologias_id_create.extend([tipologia.id_tipologia_documental for tipologia in serializador])

                    # ACTUALIZAR TIPOLOGIAS
                    tipologias_update = list(filter(lambda tipologia: tipologia['id_tipologia_documental'] != None, data))
                    if tipologias_update:
                        for tipologia in tipologias_update:
                            tipologia_existe = TipologiasDocumentales.objects.filter(id_tipologia_documental=tipologia['id_tipologia_documental']).first()
                            if tipologia_existe:
                                serializer = self.serializer_class(tipologia_existe, data=tipologia)
                                serializer.is_valid(raise_exception=True)
                                serializer.save()

                    # ELIMINAR TIPOLOGIAS
                    lista_tipologia_id = [tipologia['id_tipologia_documental'] for tipologia in tipologias_update]
                    lista_tipologia_id.extend(tipologias_id_create)
                    tipologias_eliminar = TipologiasDocumentales.objects.filter(id_trd=id_trd).exclude(id_tipologia_documental__in=lista_tipologia_id)
                    
                    # VALIDAR QUE NO SE ESTÉN USANDO LAS TIPOLOGIAS A ELIMINAR
                    tipologias_eliminar_id = [tipologia.id_tipologia_documental for tipologia in tipologias_eliminar]
                    serie_subserie_unidad_tipologia = SeriesSubSeriesUnidadesTipologias.objects.filter(id_tipologia_documental__in=tipologias_eliminar_id)
                    if serie_subserie_unidad_tipologia:
                        return Response({'success':False, 'detail':'Una o varias tipologias a eliminar ya están asociadas al TRD, por favor eliminar asociaciones primero'})
                    
                    tipologias_eliminar.delete()
                    
                    return Response({'success':True, 'detail':'Se ha realizado cambios con las tipologias'}, status=status.HTTP_201_CREATED)
                else:
                    # VALIDAR QUE NO SE ESTÉN USANDO LAS TIPOLOGIAS A ELIMINAR
                    tipologias_eliminar = TipologiasDocumentales.objects.filter(id_trd=id_trd)
                    tipologias_eliminar_id = [tipologia.id_tipologia_documental for tipologia in tipologias_eliminar]
                    serie_subserie_unidad_tipologia = SeriesSubSeriesUnidadesTipologias.objects.filter(id_tipologia_documental__in=tipologias_eliminar_id)
                    if serie_subserie_unidad_tipologia:
                        return Response({'success':False, 'detail':'Una o varias tipologias a eliminar ya están asociadas al TRD, por favor eliminar asociaciones primero'})
                    
                    tipologias_eliminar.delete()

                    return Response({'success':True, 'detail':'Se han eliminado todas las tipologias'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'success':False, 'detail':'El TRD ya está terminado, por lo cual no es posible realizar acciones sobre las tipologias'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'success':False, 'detail':'El TRD no existe'}, status=status.HTTP_404_NOT_FOUND)