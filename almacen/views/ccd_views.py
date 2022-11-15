from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from seguridad.utils import Util
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from almacen.serializers.ccd_serializers import (
    SubseriesDocSerializer,
    CCDPostSerializer,
    CCDPutSerializer,
    CCDActivarSerializer,
    CCDSerializer,
    SeriesDocPostSerializer,
    SeriesDocSerializer,
    SeriesSubseriesUnidadOrgSerializer
)
from operator import itemgetter
from seguridad.models import (
    User,
    Modulos,
    Permisos
)
from almacen.models.ccd_models import (
    CuadrosClasificacionDocumental,
    SeriesDoc,
    SubseriesDoc,
    SeriesSubseriesUnidadOrg
)
from almacen.models.organigrama_models import (
    UnidadesOrganizacionales
)

import copy

class CreateCuadroClasificacionDocumental(generics.CreateAPIView):
    serializer_class = CCDPostSerializer
    queryset = CuadrosClasificacionDocumental.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            pass
        except:
            return Response({'success': False, 'detail': 'Valide la información ingresada, el id organigrama es requerido, el nombre y la versión son requeridos y deben ser únicos'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializador = serializer.save()

        #Auditoria Crear Cuadro de Clasificación Documental
        usuario = request.user.id_usuario
        descripcion = {"Nombre": str(serializador.nombre), "Versión": str(serializador.version)}
        direccion=Util.get_client_ip(request)
        auditoria_data = {
            "id_usuario" : usuario,
            "id_modulo" : 27,
            "cod_permiso": "CR",
            "subsistema": 'GEST',
            "dirip": direccion,
            "descripcion": descripcion, 
        }
        Util.save_auditoria(auditoria_data)
        
        return Response({'success': True, 'detail': 'Cuadro de Clasificación Documental creado exitosamente', 'data': serializer.data}, status=status.HTTP_201_CREATED)


class UpdateCuadroClasificacionDocumental(generics.RetrieveUpdateAPIView):
    serializer_class = CCDPutSerializer
    queryset = CuadrosClasificacionDocumental.objects.all()
    permission_classes = [IsAuthenticated]
    #Falta validación si está siendo usado en la TRD

    def patch(self, request, pk):
        try:
            ccd = CuadrosClasificacionDocumental.objects.get(id_ccd=pk)
            previoud_ccd = copy.copy(ccd)
            pass
        except:
            return Response({'success': False, 'detail': 'No existe ningún Cuadro de Clasificación Documental con los parámetros ingresados'}, status=status.HTTP_404_NOT_FOUND)

        if ccd.fecha_terminado:
            return Response({'success': False,'detail': 'No se puede actualizar un CCD terminado'}, status=status.HTTP_403_FORBIDDEN)
            
        serializer = self.serializer_class(ccd, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            pass 
        except:
            return Response({'success': False, 'detail': 'Validar data enviada, el nombre y la versión son requeridos y deben ser únicos'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        
        # AUDITORIA DE UPDATE DE CCD
        user_logeado = request.user.id_usuario
        dirip = Util.get_client_ip(request)
        descripcion = {'nombre':str(previoud_ccd.nombre), 'version':str(previoud_ccd.version)}
        valores_actualizados={'previous':previoud_ccd, 'current':ccd}
        auditoria_data = {
            'id_usuario': user_logeado,
            'id_modulo': 27,
            'cod_permiso': 'AC',
            'subsistema': 'GEST',
            'dirip': dirip,
            'descripcion': descripcion,
            'valores_actualizados': valores_actualizados
        }
        Util.save_auditoria(auditoria_data)
        
        return Response({'success': True, 'detail': 'Cuadro de Clasificación Documental actualizado exitosamente', 'data': serializer.data}, status=status.HTTP_201_CREATED)


class FinalizarCuadroClasificacionDocumental(generics.UpdateAPIView):
    serializer_class = CCDActivarSerializer
    queryset = CuadrosClasificacionDocumental

    def put(self, request, pk):
        ccd = CuadrosClasificacionDocumental.objects.filter(id_ccd=pk).first()
        if ccd:
            #Validacion existencia del ccd a finalizar
            if ccd.fecha_terminado == None:
                unidades = UnidadesOrganizacionales.objects.filter(Q(id_organigrama=ccd.id_organigrama) & ~Q(cod_agrupacion_documental=None))
                unidades_list = [unidad.id_unidad_organizacional for unidad in unidades]
                
                series = SeriesDoc.objects.filter(id_ccd=pk)
                series_list = [serie.id_serie_doc for serie in series]

                subseries = SubseriesDoc.objects.filter(id_ccd=pk)
                subseries_list = [subserie.id_subserie_doc for subserie in subseries]


                serie_subserie_unidad = SeriesSubseriesUnidadOrg.objects.filter(id_serie_doc__in=series_list)
                print(serie_subserie_unidad)
                unidades_asignacion_list = [serie.id_unidad_organizacional.id_unidad_organizacional for serie in serie_subserie_unidad]
                series_asignacion_list = [serie.id_serie_doc.id_serie_doc for serie in serie_subserie_unidad]

                subseries_asignacion_list = [subserie.id_sub_serie_doc.id_subserie_doc for subserie in serie_subserie_unidad if subserie.id_sub_serie_doc]
                print(subseries_asignacion_list)

                if not set(unidades_list).issubset(unidades_asignacion_list):
                    return Response({'success': False, 'detail': 'Debe asociar todas las unidades'}, status=status.HTTP_400_BAD_REQUEST)

                if not set(series_list).issubset(series_asignacion_list):
                    return Response({'success': False, 'detail': 'Debe asociar todas las series'}, status=status.HTTP_400_BAD_REQUEST)

                #Agregar validación para cuando una lista viene vacia
                if not set(subseries_list).issubset(set(subseries_asignacion_list)):
                    return Response({'success': False, 'detail': 'Debe asociar todas las subseries'}, status=status.HTTP_400_BAD_REQUEST)

                ccd.fecha_terminado = datetime.now()
                ccd.save()
                return Response({'success': True, 'detail': 'Finalizado el CCD'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'success': False, 'detail': 'Ya se encuentra finalizado este CCD'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'success': False, 'detail': 'No se encontró ningún CCD con estos parámetros'}, status=status.HTTP_404_NOT_FOUND)    
        
        

class GetCuadroClasificacionDocumental(generics.ListAPIView):
    serializer_class = CCDSerializer  
    queryset = CuadrosClasificacionDocumental.objects.all()

    def get(self, request):
        consulta = request.query_params.get('pk')
        if consulta == None:
            ccds = CuadrosClasificacionDocumental.objects.all().values()
            if len(ccds) == 0:
                return Response({'success': True, 'detail' : 'Aún no hay Cuadros de Clasificación Documental registrados'}, status=status.HTTP_200_OK)
            return Response({'success': True, 'cuadros de Clasificación Documental': ccds}, status=status.HTTP_200_OK) 
        ccd = CuadrosClasificacionDocumental.objects.filter(id_ccd=consulta).values()
        if len(ccd) == 0:
            return Response({'success': False, 'detail' : 'No se encontró el Cuadro de Clasificación Documental ingresado'}, status=status.HTTP_404_NOT_FOUND)
        series = SeriesDoc.objects.filter(id_ccd=int(consulta)).values()
        subseries = 'No hay subseries'
        if len(series) == 0:
            series = 'No hay series registradas'
            subseries = 'No hay subseries registradas'
            datos_finales = {'Cuadro de Clasificación Documental' : ccd, 'Series' : series, 'Subseries' : subseries}
            return Response({'success': True, 'Cuadro de Clasificación Documental' : datos_finales}, status=status.HTTP_200_OK)
        subseries = SubseriesDoc.objects.filter(id_ccd=int(consulta)).values()
        if len(subseries) == 0:
            subseries = 'No hay subseries registradas'
            datos_finales = {'Cuadro de Clasificación Documental' : ccd, 'Series' : series, 'Subseries' : subseries}
            return Response({'success': True, 'Cuadro de Clasificación Documental' : datos_finales}, status=status.HTTP_200_OK)
        datos_finales = {'Cuadro de Clasificación Documental' : ccd, 'series' : series, 'Subseries' : subseries}
        return Response({'success': True,'Cuadro de Clasificación Documental' : datos_finales}, status=status.HTTP_200_OK)

class GetCCDTerminado(generics.ListAPIView):
    serializer_class = CCDSerializer  
    queryset = CuadrosClasificacionDocumental.objects.filter(~Q(fecha_terminado = None))

#Crear Series documentales
class CreateSeriesDoc(generics.CreateAPIView):
    serializer_class = SeriesDocPostSerializer
    queryset = SeriesDoc.objects.all()
    
    def post(self, request):
        if request.data == []:
            return Response({"Error" : "Ingresó una lista vacía"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data,list))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        usuario = request.user.id_usuario
        user = User.objects.get(id_usuario = usuario)
        modulo = Modulos.objects.get(id_modulo = 5)
        permiso = Permisos.objects.get(cod_permiso = 'BO')
        direccion_ip = Util.get_client_ip(request)
        descripcion =  {"Series ingresadas" : request.data}
        auditoria_data = {
            'id_usuario': request.user.id_usuario,
            'id_modulo': 5,
            'cod_permiso': 'CR',
            'subsistema': 'SEGU',
            'dirip': direccion_ip,
            'descripcion': descripcion
        }
            
        Util.save_auditoria(auditoria_data)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class GetSeriesDoc(generics.ListAPIView):
    serializer_class = SeriesDocSerializer
    
    def get(self, request):
        dato_buscado = request.query_params.get('pk')
        if dato_buscado == None:
            series_doc = SeriesDoc.objects.all().values()
            if len(series_doc) == 0:
                return Response({'Error' : 'Aún no hay series documentales registradas'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'Series documentales' : series_doc}, status=status.HTTP_200_OK) 
        series_doc = SeriesDoc.objects.filter(id_ccd=int(dato_buscado)).values()
        if len(series_doc) == 0:
            return Response({'Error' : 'No se encontró la serie documental ingresada'}, status=status.HTTP_404_NOT_FOUND)
        ccd = CuadrosClasificacionDocumental.objects.filter(id_ccd = dato_buscado).values()
        datos_finales = {"CCD" : ccd, "Series documentales" : series_doc}
        return Response(datos_finales, status=status.HTTP_200_OK)


class CreateSubseriesDoc(generics.CreateAPIView):
    serializer_class = SubseriesDocSerializer
    queryset = SubseriesDoc.objects.all()
    
    def post(self, request, id_ccd):
        data = request.data
        subseries = SubseriesDoc.objects.filter(id_ccd=id_ccd)
        ccd = CuadrosClasificacionDocumental.objects.filter(id_ccd=id_ccd).first()
        if ccd:
            if not ccd.fecha_terminado:
                if data:
                    # VALIDAR QUE EL ID_CCD SEA EL MISMO
                    ccd_list = [subserie['id_ccd'] for subserie in data]
                    if len(set(ccd_list)) != 1:
                        return Response({'success':False, 'detail':'Debe validar que las subseries pertenezcan a un mismo CCD'}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        print(ccd_list[0])
                        if ccd_list[0] != int(id_ccd):
                            return Response({'success':False, 'detail':'El id ccd de la petición debe ser igual al enviado en url'}, status=status.HTTP_400_BAD_REQUEST)
                                     
                    # VALIDAR QUE LOS CODIGOS SEAN UNICOS
                    codigos_list = [subserie['codigo'] for subserie in data]
                    if len(codigos_list) != len(set(codigos_list)):
                        return Response({'success':False, 'detail':'Debe validar que los códigos de las subseries sean únicos'}, status=status.HTTP_400_BAD_REQUEST)
                    
                    # VALIDAR QUE LOS NOMBRES SEAN UNICOS
                    nombres_list = [subserie['nombre'] for subserie in data]
                    if len(nombres_list) != len(set(nombres_list)):
                        return Response({'success':False, 'detail':'Debe validar que los nombres de las subseries sean únicos'}, status=status.HTTP_400_BAD_REQUEST)
                    
                    # CREAR SUBSERIES
                    subseries_create = list(filter(lambda subserie: subserie['id_subserie_doc'] == None, data))
                    subseries_id_create = []
                    if subseries_create:
                        serializer = self.serializer_class(data=subseries_create, many=True)
                        serializer.is_valid(raise_exception=True)
                        serializador = serializer.save()
                        subseries_id_create.extend([subserie.id_subserie_doc for subserie in serializador])

                    # ACTUALIZAR SUBSERIES
                    subseries_update = list(filter(lambda subserie: subserie['id_subserie_doc'] != None, data))
                    if subseries_update:
                        for subserie in subseries_update:
                            subserie_existe = SubseriesDoc.objects.filter(id_subserie_doc=subserie['id_subserie_doc']).first()
                            if subserie_existe:
                                serializer = self.serializer_class(subserie_existe, data=subserie)
                                serializer.is_valid(raise_exception=True)
                                serializer.save()

                    # ELIMINAR SUBSERIES
                    lista_subseries_id = [subserie['id_subserie_doc'] for subserie in subseries_update]
                    lista_subseries_id.extend(subseries_id_create)
                    subseries_eliminar = SubseriesDoc.objects.filter(id_ccd=id_ccd).exclude(id_subserie_doc__in=lista_subseries_id)
                    subseries_eliminar.delete()
                    
                    return Response({'success':True, 'detail':'Se ha realizado cambios con las subseries'}, status=status.HTTP_201_CREATED)
                else:
                    subseries.delete()

                    return Response({'success':True, 'detail':'Se han eliminado todas las subseries'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'success':False, 'detail':'El CCD ya está terminado, por lo cual no es posible realizar acciones sobre las subseries'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'success':False, 'detail':'El CCD no existe'}, status=status.HTTP_404_NOT_FOUND)

class GetSubseries(generics.ListAPIView):
    serializer_class = SubseriesDocSerializer
    queryset = SubseriesDoc.objects.all()
    
    def get(self, request, id_ccd):
        ccd = CuadrosClasificacionDocumental.objects.filter(id_ccd=id_ccd).first()
        if ccd:
            subseries = SubseriesDoc.objects.filter(id_ccd=id_ccd)
            serializer = self.serializer_class(subseries, many=True)
            return Response({'success':True, 'detail':serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'success':False, 'detail':'Debe consultar por un CCD válido'}, status=status.HTTP_404_NOT_FOUND)
class AsignarSeriesYSubseriesAUnidades(generics.UpdateAPIView):
    serializer_class = SeriesSubseriesUnidadOrgSerializer
    
    def put(self, request):
        datos_ingresados = request.data
        if datos_ingresados == []:
            return Response({"Error" : "Ingresó una lista vacía"}, status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(datos_ingresados['id_unidad_organizacional'], int):
             return Response({"Error" : "Unidad organizacional debe ser un número entero"}, status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(datos_ingresados['id_serie_doc'], int):
             return Response({"Error" : "La serie documental debe ser un número entero"}, status=status.HTTP_400_BAD_REQUEST)
        unidad_organizacional = UnidadesOrganizacionales.objects.filter(id_unidad_organizacional=datos_ingresados['id_unidad_organizacional']).first()
        if unidad_organizacional == None:
            return Response({"Error" : "No existe esa unidad organizacional"}, status=status.HTTP_400_BAD_REQUEST)
        serie = SeriesDoc.objects.filter(id_serie_doc=datos_ingresados['id_serie_doc']).first()
        if serie == None:
            return Response({"Error" : "No existe esa serie documental"}, status=status.HTTP_400_BAD_REQUEST)
        subseries = datos_ingresados['subseries']
        datos = []
        for i in subseries:
            subserie = SubseriesDoc.objects.filter(id_subserie_doc=i).first()
            if not isinstance(i, int):
                return Response({"Error" : "Las subseries documentales deben ser un número entero", "Subserie erronea" : i}, status=status.HTTP_400_BAD_REQUEST)
            if subserie == None:
                return Response({"Error" : "Una de las series documentales no existe", "Serie documental inexistente" : i}, status=status.HTTP_400_BAD_REQUEST)
            datos.append({"id_unidad_organizacional" : unidad_organizacional.id_unidad_organizacional, "id_serie_doc" : serie.id_serie_doc, "id_sub_serie_doc" : subserie.id_subserie_doc})
        instance = SeriesSubseriesUnidadOrg.objects.filter(id_unidad_organizacional=unidad_organizacional.id_unidad_organizacional).filter(id_serie_doc=serie.id_serie_doc)
        aux = (SeriesSubseriesUnidadOrg.objects.filter(id_unidad_organizacional=unidad_organizacional.id_unidad_organizacional).filter(id_serie_doc=serie.id_serie_doc)).values()
        borrados=[]
        if instance != None:
            for i in aux:
                borrados.append(i['id_sub_serie_doc_id'])
                print(i['id_sub_serie_doc_id'])
            for i in instance:
                i.delete()
            
        datos_borrados = {"Unidad organizacional" : str(datos_ingresados['id_unidad_organizacional']), "Serie documental" : str(datos_ingresados['id_serie_doc']), "Subseries documentales" : str(borrados)}
        serializer = self.get_serializer(data=datos, many=isinstance(datos,list))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        usuario = request.user.id_usuario
        user = User.objects.get(id_usuario = usuario)
        modulo = Modulos.objects.get(id_modulo = 5)
        permiso = Permisos.objects.get(cod_permiso = 'BO')
        direccion_ip = Util.get_client_ip(request)
        descripcion =  {"Datos insertados" : {"Unidad organizacional" : str(datos_ingresados['id_unidad_organizacional']), "Serie documental" : str(datos_ingresados['id_serie_doc']), "Subseries documentales" : str(datos_ingresados['subseries'])}, "Datos borrados" : datos_borrados}
        auditoria_data = {
            'id_usuario': request.user.id_usuario,
            'id_modulo': 5,
            'cod_permiso': 'CR',
            'subsistema': 'SEGU',
            'dirip': direccion_ip,
            'descripcion': descripcion
        }
            
        Util.save_auditoria(auditoria_data)
            
        return Response({"Mensaje" : "Datos guardados con éxito", "Datos" : serializer.data}, status=status.HTTP_201_CREATED)
    
class GetAsignaciones(generics.ListAPIView):
    serializer_class = SeriesSubseriesUnidadOrgSerializer
    
    def get(self, request):
        dato_consultado = request.query_params.get('ccd')
        if dato_consultado == None:
            return Response({"Error" : "Debe ingresar algún valor"}, status=status.HTTP_400_BAD_REQUEST)
        try: 
            int(dato_consultado)
            pass
        except:
            return Response({"Error" : "El id de la ccd debe ser un número entero"}, status=status.HTTP_400_BAD_REQUEST)
        ccd = (CuadrosClasificacionDocumental.objects.filter(id_ccd=dato_consultado).values())
        if len(ccd) == 0:
            return Response({"Mensaje Error" : "Esta CCD no existe"})
        else:
            ccd = ccd[0]
        series_doc = (SeriesDoc.objects.filter(id_ccd=ccd['id_ccd']).values())
        datos_salida = {"ccd" : ccd, "Subseries documentales" : series_doc}
        cont = 0
        cuentame = 0
        lista_serie_en_asignaciones = []
        nuevo=[]
        vector_aux = []
        for serie in series_doc:
            instancia_series_doc = (SeriesDoc.objects.filter(id_serie_doc=serie['id_serie_doc']).first())
            volatil = SeriesSubseriesUnidadOrg.objects.filter(id_serie_doc_id=instancia_series_doc.id_serie_doc).values()
            ordenados = sorted(volatil, key=lambda a : a['id_unidad_organizacional_id'])
            
            for i in ordenados:
                nuevo.append(i)
                if cont < (len(ordenados)-1):
                    cont = cont + 1
                
                aux = ordenados[cont]
                if i['id_unidad_organizacional_id'] != aux['id_unidad_organizacional_id']:
                    cuentame = cuentame + 1
                    vector_aux.append(nuevo)
                    nuevo = []

            if volatil:
                vector_aux.append(nuevo)
                contador = 0
                for i in vector_aux:
                    contador = contador + 1
                    ultimos = []
                    for iterable in i:
                        ultimos.append(iterable['id_sub_serie_doc_id'])
                    datos_salida = {"Unidad documental" + str(((i)[0])['id_unidad_organizacional_id']) : ((i)[0])['id_unidad_organizacional_id'], "Serie documental" + str(((i)[0])['id_serie_doc_id']) : ((i)[0])['id_serie_doc_id'], "Subseries" : ultimos}
                    lista_serie_en_asignaciones.append(datos_salida)
                
            vector_aux =[]
            nuevo = []    
            cont = 0
            
        return Response({"Series y subseries asignadas a unidades organizacioneales en la CCD" + str(dato_consultado) : lista_serie_en_asignaciones}, status=status.HTTP_201_CREATED)
