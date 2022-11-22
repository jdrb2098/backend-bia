from rest_framework import status
from django.db.models import Q
import copy
from datetime import datetime
from rest_framework import generics
from rest_framework.response import Response
from seguridad.utils import Util
from rest_framework.permissions import IsAuthenticated
from gestion_documental.serializers.trd_serializers import (
    TipologiasDocumentalesSerializer,
    TRDSerializer,
    TRDPostSerializer,
    TRDPutSerializer,
    TRDFinalizarSerializer
)
from gestion_documental.models.ccd_models import (
    SeriesSubseriesUnidadOrg,
    CuadrosClasificacionDocumental,
    SeriesDoc
)
from almacen.models.organigrama_models import (
    Organigramas
)
from gestion_documental.models.trd_models import (
    TablaRetencionDocumental,
    TipologiasDocumentales,
    SeriesSubSUnidadOrgTRDTipologias
)

class UpdateTipologiasDocumentales(generics.UpdateAPIView):
    serializer_class = TipologiasDocumentalesSerializer
    queryset = TipologiasDocumentales.objects.all()
    
    def put(self, request, id_trd):
        data = request.data
        trd = TablaRetencionDocumental.objects.filter(id_trd=id_trd).first()
        if trd:
            if not trd.fecha_terminado:
                if data:
                    # VALIDAR QUE EL ID_TRD SEA EL MISMO
                    trd_list = [tipologia['id_trd'] for tipologia in data]
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
                    serie_subserie_unidad_tipologia = SeriesSubSUnidadOrgTRDTipologias.objects.filter(id_tipologia_doc__in=tipologias_eliminar_id)
                    if serie_subserie_unidad_tipologia:
                        return Response({'success':False, 'detail':'Una o varias tipologias a eliminar ya están asociadas al TRD, por favor eliminar asociaciones primero'}, status=status.HTTP_403_FORBIDDEN)
                    
                    tipologias_eliminar.delete()
                    
                    return Response({'success':True, 'detail':'Se ha realizado cambios con las tipologias'}, status=status.HTTP_201_CREATED)
                else:
                    # VALIDAR QUE NO SE ESTÉN USANDO LAS TIPOLOGIAS A ELIMINAR
                    tipologias_eliminar = TipologiasDocumentales.objects.filter(id_trd=id_trd)
                    tipologias_eliminar_id = [tipologia.id_tipologia_documental for tipologia in tipologias_eliminar]
                    serie_subserie_unidad_tipologia = SeriesSubSUnidadOrgTRDTipologias.objects.filter(id_tipologia_doc__in=tipologias_eliminar_id)
                    if serie_subserie_unidad_tipologia:
                        return Response({'success':False, 'detail':'Una o varias tipologias a eliminar ya están asociadas al TRD, por favor eliminar asociaciones primero'}, status=status.HTTP_403_FORBIDDEN)
                    
                    tipologias_eliminar.delete()

                    return Response({'success':True, 'detail':'Se han eliminado todas las tipologias'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'success':False, 'detail':'El TRD ya está terminado, por lo cual no es posible realizar acciones sobre las tipologias'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'success':False, 'detail':'El TRD no existe'}, status=status.HTTP_404_NOT_FOUND)

class GetTipologiasDocumentales(generics.ListAPIView):
    serializer_class = TipologiasDocumentalesSerializer
    queryset = TipologiasDocumentales.objects.all()
    
    def get(self, request, id_trd):
        trd = TablaRetencionDocumental.objects.filter(id_trd=id_trd).first()
        if trd:
            tipologias = TipologiasDocumentales.objects.filter(id_trd=id_trd)
            serializer = self.serializer_class(tipologias, many=True)
            return Response({'success':True, 'detail':serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'success':False, 'detail':'Debe consultar por un TRD válido'}, status=status.HTTP_404_NOT_FOUND)
        

#Tabla de Retencion Documental

class GetTablaRetencionDocumental(generics.ListAPIView):
    serializer_class = TRDSerializer
    queryset = TablaRetencionDocumental.objects.all()

class GetTablaRetencionDocumentalTerminados(generics.ListAPIView):
    serializer_class = TRDSerializer
    queryset = TablaRetencionDocumental.objects.filter(~Q(fecha_terminado=None))

class PostTablaRetencionDocumental(generics.CreateAPIView):
    serializer_class = TRDPostSerializer
    queryset = TablaRetencionDocumental
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            pass
        except:
            return Response({'success': False, 'detail': 'Valide la información ingresada, el id_ccd es requerido, el nombre y la versión son requeridos y deben ser únicos'}, status=status.HTTP_400_BAD_REQUEST)
        
        #Validación de seleccionar solo ccd terminados
        ccd = serializer.validated_data.get('id_ccd')
        ccd_instance = CuadrosClasificacionDocumental.objects.filter(id_ccd=ccd.id_ccd).first()
        if ccd_instance:
            if ccd_instance.fecha_terminado == None:
                return Response({'success': False, 'detail': 'No se pueden seleccionar Cuadros de Clasificación Documental que no estén terminados'}, status=status.HTTP_403_FORBIDDEN)
        
            serializado = serializer.save()

            #Auditoria Crear Tabla de Retención Documental
            usuario = request.user.id_usuario
            descripcion = {"Nombre": str(serializado.nombre), "Versión": str(serializado.version)}
            direccion=Util.get_client_ip(request)
            auditoria_data = {
                "id_usuario" : usuario,
                "id_modulo" : 29,
                "cod_permiso": "CR",
                "subsistema": 'GEST',
                "dirip": direccion,
                "descripcion": descripcion, 
            }
            Util.save_auditoria(auditoria_data)

            return Response({'success': True, 'detail': 'TRD creada exitosamente'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'success': False, 'detail': 'No existe un Cuadro de Clasificación Documental con el id_ccd enviado'}, status=status.HTTP_400_BAD_REQUEST)

class UpdateTablaRetencionDocumental(generics.RetrieveUpdateAPIView):
    serializer_class = TRDPutSerializer
    queryset = TablaRetencionDocumental.objects.all()
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            trd = TablaRetencionDocumental.objects.get(id_trd=pk)
            previoud_trd = copy.copy(trd)
            pass
        except:
            return Response({'success': False, 'detail': 'No existe ninguna Tabla de Retención Documental con los parámetros ingresados'}, status=status.HTTP_404_NOT_FOUND)

        if trd.fecha_terminado:
            return Response({'success': False,'detail': 'No se puede actualizar una TRD terminada'}, status=status.HTTP_403_FORBIDDEN)
            
        serializer = self.serializer_class(trd, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            pass 
        except:
            return Response({'success': False, 'detail': 'Validar data enviada, el nombre y la versión son requeridos y deben ser únicos'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        
        # AUDITORIA DE UPDATE DE CCD
        user_logeado = request.user.id_usuario
        dirip = Util.get_client_ip(request)
        descripcion = {'nombre':str(previoud_trd.nombre), 'version':str(previoud_trd.version)}
        valores_actualizados={'previous':previoud_trd, 'current':trd}
        auditoria_data = {
            'id_usuario': user_logeado,
            'id_modulo': 29,
            'cod_permiso': 'AC',
            'subsistema': 'GEST',
            'dirip': dirip,
            'descripcion': descripcion,
            'valores_actualizados': valores_actualizados
        }
        Util.save_auditoria(auditoria_data)
        
        return Response({'success': True, 'detail': 'Tabla de Retención Documental actualizado exitosamente', 'data': serializer.data}, status=status.HTTP_201_CREATED)

# class FinalizarTablaRetencionDocumental(generics.RetrieveUpdateAPIView):
#     serializer_class = TRDFinalizarSerializer
#     queryset = TablaRetencionDocumental

#     def put(self, request, id_trd):
#         trd = TablaRetencionDocumental.objects.filter(id_trd=id_trd).first()
#         if trd:
#             if trd.fecha_terminado == None:
#                 #Obtiene el id de las tipologias existentes relacionadas a la TRD
#                 tipologias = TipologiasDocumentales.objects.filter(id_trd=id_trd)
#                 tipologias_list = [tipologia.id_tipologia_documental for tipologia in tipologias]

#                 #Obtiene el id de la seriesubserieunidad existentes relacionadas con el ccd asociado a la TRD
#                 ccd_trd = CuadrosClasificacionDocumental.objects.get(id_ccd=trd.id_ccd.id_ccd)
#                 series_ccd_trd = SeriesDoc.objects.filter(id_ccd=ccd_trd.id_ccd)
#                 series_ccd_trd_list = [serie.id_serie_doc for serie in series_ccd_trd]
#                 serie_subserie_unidadorg = SeriesSubseriesUnidadOrg.objects.filter(id_serie_doc__in=series_ccd_trd_list)
#                 serie_subserie_unidadorg_list = [serie.id_serie_subserie_doc for serie in serie_subserie_unidadorg]


#                 # Busqueda mediante la tipologia, valor clave que contiene la trd directa
#                 serie_subserie_tipologia_list = SeriesSubSeriesUnidadesTipologias.objects.filter(id_tipologia_documental__in=tipologias_list)

#                 #Id de conexiones de ccd conectadas en TRD
#                 series_unidades_asignacion_list = [serie.id_serie_subserie_doc.id_serie_subserie_doc for serie in serie_subserie_tipologia_list]

#                 #Id de tipologias relacionadas conectadas
#                 tipologias_asignacion_list = [serie.id_tipologia_documental.id_tipologia_documental for serie in serie_subserie_tipologia_list]

#                 #Valida que lo existente asociado a esa trd esté asociado en la tabla intermedia
#                 if not set(tipologias_list).issubset(tipologias_asignacion_list):
#                     tipologias_difference_list = [tipologia for tipologia in tipologias_list if tipologia not in tipologias_asignacion_list]
#                     tipologias_difference_instance = TipologiasDocumentales.objects.filter(id_tipologia_documental__in=tipologias_difference_list).values()
#                     return Response({'success': False, 'detail': 'Debe asociar todas las tipologias de esta TRD', 'Tipologias sin asignar':tipologias_difference_instance}, status=status.HTTP_400_BAD_REQUEST)
                    
                
#                 if not set(serie_subserie_unidadorg_list).issubset(series_unidades_asignacion_list):
#                     serie_subser_unidad_difference_list = [serie_sub_uni for serie_sub_uni in serie_subserie_unidadorg_list if serie_sub_uni not in series_unidades_asignacion_list]
#                     serie_sub_unidad_difference_instance = SeriesSubseriesUnidadOrg.objects.filter(id_serie_subserie_doc__in=serie_subser_unidad_difference_list).values()
#                     return Response({'success': False, 'detail': 'Debe asociar todas las series subseries unidades del CCD asociado a esta TRD', 'Series Subseries Unidades sin asignar': serie_sub_unidad_difference_instance}, status=status.HTTP_400_BAD_REQUEST)

#                 #Poner Fecha Terminado
#                 trd.fecha_terminado = datetime.now()
#                 trd.save()
#                 return Response({'success': True, 'detail': 'Finalizado el CCD'}, status=status.HTTP_201_CREATED)
#             else:
#                 return Response({'success': False, 'detail': 'Ya se encuentra finalizado esta TRD'}, status=status.HTTP_404_NOT_FOUND)
#         else:
#             return Response({'success': False, 'detail': 'No se encontró ninguna TRD con estos parámetros'}, status=status.HTTP_404_NOT_FOUND)    

class Activar(generics.UpdateAPIView):
    serializer_class =TRDSerializer
    queryset=TablaRetencionDocumental.objects.all()
    permission_classes = [IsAuthenticated]
    
    def put(self,request,pk):
        user_logeado = request.user.id_usuario
        dirip = Util.get_client_ip(request)
        
        trd_remplazante=TablaRetencionDocumental.objects.filter(id_trd=pk).first()
        
        if trd_remplazante:
            if trd_remplazante.fecha_terminado:
                if not trd_remplazante.actual:
                    try:
                        ccd_remplazante=CuadrosClasificacionDocumental.objects.filter(id_ccd=trd_remplazante.id_ccd.id_ccd).first()
                        organigrama_remplazante=Organigramas.objects.filter(id_organigrama=trd_remplazante.id_ccd.id_organigrama.id_organigrama).first()
                        
                        trd_a_remplazar=TablaRetencionDocumental.objects.filter(actual=True).first()
                        ccd_a_remplazar=CuadrosClasificacionDocumental.objects.filter(actual=True).first()
                        organigrama_a_remplazar=Organigramas.objects.filter(actual=True).first()
                        
                        previous_remplazante_trd=copy.copy(trd_remplazante)
                        previous_a_remplazar_trd=copy.copy(trd_a_remplazar)
                        previous_remplazante_ccd=copy.copy(ccd_remplazante)
                        previous_a_remplazar_ccd=copy.copy(ccd_a_remplazar)
                        previous_remplazante_org=copy.copy(organigrama_remplazante)
                        previous_a_remplazar_org=copy.copy(organigrama_a_remplazar)
                        
                        if trd_a_remplazar:
                            trd_remplazante.actual=True
                            trd_a_remplazar.actual=False
                            ccd_remplazante.actual=True
                            organigrama_remplazante.actual=True
                            
                            trd_remplazante.fecha_puesta_produccion=datetime.now()
                            trd_remplazante.fecha_retiro_produccion=None
                            trd_a_remplazar.fecha_retiro_produccion=datetime.now()
                            trd_a_remplazar.fecha_puesta_produccion=None
                            
                            if ccd_remplazante.id_ccd != ccd_a_remplazar.id_ccd:
                                ccd_a_remplazar.actual=False
                                ccd_a_remplazar.fecha_retiro_produccion=datetime.now()
                                ccd_a_remplazar.fecha_puesta_produccion=None
                                ccd_remplazante.fecha_puesta_produccion=datetime.now()
                                ccd_remplazante.fecha_retiro_produccion=None
                                
                                #auditoria de CCD  activado
                                descripcion = {"nombre":str(ccd_remplazante.nombre),"versión":str(ccd_remplazante.version)}
                                valores_actualizados={'previous':previous_remplazante_ccd, 'current':ccd_remplazante}
                                auditoria_data = {
                                    'id_usuario': user_logeado,
                                    'id_modulo': 28,
                                    'cod_permiso': 'AC',
                                    'subsistema': 'GEST',
                                    'dirip': dirip,
                                    'descripcion': descripcion,
                                    'valores_actualizados': valores_actualizados
                                }
                                Util.save_auditoria(auditoria_data)
                                
                                #auditoria de CCD desactivado
                                descripcion = {"nombre":str(ccd_a_remplazar.nombre),"versión":str(ccd_a_remplazar.version)}
                                valores_actualizados={'previous':previous_a_remplazar_ccd, 'current':ccd_a_remplazar}
                                auditoria_data = {
                                    'id_usuario': user_logeado,
                                    'id_modulo': 28,
                                    'cod_permiso': 'AC',
                                    'subsistema': 'GEST',
                                    'dirip': dirip,
                                    'descripcion': descripcion,
                                    'valores_actualizados': valores_actualizados
                                }
                                Util.save_auditoria(auditoria_data)
                                
                            if organigrama_remplazante.id_organigrama != organigrama_a_remplazar.id_organigrama:
                                organigrama_a_remplazar.actual=False
                                organigrama_a_remplazar.fecha_retiro_produccion=datetime.now()
                                organigrama_a_remplazar.fecha_puesta_produccion=None
                                organigrama_remplazante.fecha_puesta_produccion=datetime.now()
                                organigrama_remplazante.fecha_retiro_produccion=None
                                
                                #auditoria de organigrama activado
                                descripcion = {"nombre":str(organigrama_remplazante.nombre),"versión":str(organigrama_remplazante.version)}
                                valores_actualizados={'previous':previous_remplazante_org, 'current':organigrama_remplazante}
                                auditoria_data = {
                                    'id_usuario': user_logeado,
                                    'id_modulo': 16,
                                    'cod_permiso': 'AC',
                                    'subsistema': 'TRSV',
                                    'dirip': dirip,
                                    'descripcion': descripcion,
                                    'valores_actualizados': valores_actualizados
                                }
                                Util.save_auditoria(auditoria_data)
                                
                                #auditoria de Organigrama desactivado
                                descripcion = {"nombre":str(organigrama_a_remplazar.nombre),"versión":str(organigrama_a_remplazar.version)}
                                valores_actualizados={'previous':previous_a_remplazar_org, 'current':organigrama_a_remplazar}
                                auditoria_data = {
                                    'id_usuario': user_logeado,
                                    'id_modulo': 16,
                                    'cod_permiso': 'AC',
                                    'subsistema': 'TRSV',
                                    'dirip': dirip,
                                    'descripcion': descripcion,
                                    'valores_actualizados': valores_actualizados
                                }
                                Util.save_auditoria(auditoria_data)
                                
                            trd_a_remplazar.save()
                            trd_remplazante.save()
                            ccd_a_remplazar.save()
                            ccd_remplazante.save()
                            organigrama_a_remplazar.save()
                            organigrama_remplazante.save()
                            
                            #auditoria de TRD activado
                            descripcion = {"nombre":str(trd_remplazante.nombre),"versión":str(trd_remplazante.version)}
                            valores_actualizados={'previous':previous_remplazante_trd, 'current':trd_remplazante}
                            auditoria_data = {
                                'id_usuario': user_logeado,
                                'id_modulo': 30,
                                'cod_permiso': 'AC',
                                'subsistema': 'GEST',
                                'dirip': dirip,
                                'descripcion': descripcion,
                                'valores_actualizados': valores_actualizados
                            }
                            Util.save_auditoria(auditoria_data)
                            
                            #auditoria de TRD desactivado
                            descripcion = {"nombre":str(trd_a_remplazar.nombre),"versión":str(trd_a_remplazar.version)}
                            valores_actualizados={'previous':previous_a_remplazar_trd, 'current':trd_a_remplazar}
                            auditoria_data = {
                                'id_usuario': user_logeado,
                                'id_modulo': 30,
                                'cod_permiso': 'AC',
                                'subsistema': 'GEST',
                                'dirip': dirip,
                                'descripcion': descripcion,
                                'valores_actualizados': valores_actualizados
                            }
                            Util.save_auditoria(auditoria_data)
                        
                            return Response({'success':True,'detail': 'Activación de instrumento archivístico'}, status=status.HTTP_200_OK)
                        else:
                            #primer organigrama activado
                            trd_remplazante.actual=True
                            ccd_remplazante.actual=True
                            organigrama_remplazante.actual=True
                            trd_remplazante.fecha_puesta_produccion=datetime.now()
                            ccd_remplazante.fecha_puesta_produccion=datetime.now()
                            organigrama_remplazante.fecha_puesta_produccion=datetime.now()
                            trd_remplazante.save()
                            ccd_remplazante.save()
                            organigrama_remplazante.save()

                            #auditoria de TRD activado
                            user_logeado = request.user.id_usuario
                            dirip = Util.get_client_ip(request)
                            descripcion = {"nombre":str(trd_remplazante.nombre),"versión":str(trd_remplazante.version)}
                            valores_actualizados={'previous':previous_remplazante_trd, 'current':trd_remplazante}
                            auditoria_data = {
                                'id_usuario': user_logeado,
                                'id_modulo': 30,
                                'cod_permiso': 'AC',
                                'subsistema': 'GEST',
                                'dirip': dirip,
                                'descripcion': descripcion,
                                'valores_actualizados': valores_actualizados
                            }
                            Util.save_auditoria(auditoria_data)
                            
                            #auditoria de CCD  activado
                            descripcion = {"nombre":str(ccd_remplazante.nombre),"versión":str(ccd_remplazante.version)}
                            valores_actualizados={'previous':previous_remplazante_ccd, 'current':ccd_remplazante}
                            auditoria_data = {
                                'id_usuario': user_logeado,
                                'id_modulo': 28,
                                'cod_permiso': 'AC',
                                'subsistema': 'GEST',
                                'dirip': dirip,
                                'descripcion': descripcion,
                                'valores_actualizados': valores_actualizados
                            }
                            Util.save_auditoria(auditoria_data)
                            
                            #auditoria de organigrama activado
                            descripcion = {"nombre":str(organigrama_remplazante.nombre),"versión":str(organigrama_remplazante.version)}
                            valores_actualizados={'previous':previous_remplazante_org, 'current':organigrama_remplazante}
                            auditoria_data = {
                                'id_usuario': user_logeado,
                                'id_modulo': 16,
                                'cod_permiso': 'AC',
                                'subsistema': 'TRSV',
                                'dirip': dirip,
                                'descripcion': descripcion,
                                'valores_actualizados': valores_actualizados
                            }
                            Util.save_auditoria(auditoria_data)
                            
                            return Response({'success':True,'detail': 'Primer instrumento archivístico activado'}, status=status.HTTP_200_OK)
                    except:
                        return Response({'success':False, 'detail':'Ocurrió un error al activar. Valide el TRD, CDD y Organigrama'},status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'success':False,'detail':'Este instrumento archivístico ya se encuentra activo'},status=status.HTTP_403_FORBIDDEN)
            else:    
                return Response({'success':False,'detail': 'No se puede activar TRD si no se encuentra finalizado'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'success':False,'detail':'No existe ningún TRD con este ID'},status=status.HTTP_403_FORBIDDEN)