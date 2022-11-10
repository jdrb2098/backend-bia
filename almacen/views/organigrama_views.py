from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from itertools import groupby
from seguridad.utils import Util
from datetime import date
import copy
from operator import itemgetter
from almacen.serializers.organigrama_serializers import (
    NivelesPostSerializer, 
    OrganigramaSerializer, 
    UnidadesPutSerializer, 
    OrganigramaActivateSerializer, 
    NivelesUpdateSerializer, 
    NivelesGetSerializer,
    UnidadesGetSerializer
    )
from almacen.models.organigrama_models import (
    Organigramas,
    UnidadesOrganizacionales,
    NivelesOrganigrama
    )

class CreateNiveles(generics.CreateAPIView):
    serializer_class = NivelesPostSerializer
    queryset = NivelesOrganigrama.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data, many=True)
        try:
            serializer.is_valid(raise_exception=True)
            pass
        except:
            return Response({'success': False, 'detail': 'Valide los datos ingresados, el nombre y el orden del nivel deben ser únicos.'}, status=status.HTTP_400_BAD_REQUEST)  
        try:
            serializer.save()
            pass
        except:
            return Response({'success': False, 'detail': 'No se pudo guardar este nivel'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': True, 'detail': serializer.data}, status=status.HTTP_201_CREATED)


class UpdateNiveles(generics.UpdateAPIView):
    serializer_class = NivelesUpdateSerializer
    queryset = NivelesOrganigrama.objects.all()

    def put(self, request, id_organigrama):
        data = request.data

        #VALIDA SI NO HA CREADO NINGÚN NIVEL
        if not data:
            return Response({'success': False, 'detail': 'No se puede guardar sin crear al menos un nivel'}, status=status.HTTP_400_BAD_REQUEST)
        
        #VALIDACION DE ORGANIGRAMA
        try:
            organigrama = Organigramas.objects.get(id_organigrama=id_organigrama)
            pass
        except:
            return Response({'success': False, 'detail': 'No se pudo encontrar un organigrama con el parámetro ingresado'}, status=status.HTTP_400_BAD_REQUEST)

        #VALIDACION DE FECHA DE TERMINADO
        if organigrama.fecha_terminado != None:
            return Response({'success': False, 'detail': 'El organigrama ya está terminado, por lo cúal no es posible realizar acciones sobre los niveles'}, status=status.HTTP_403_FORBIDDEN)

        #ELIMINACION DE TODOS LOS NIVELES
        niveles = NivelesOrganigrama.objects.filter(id_organigrama=id_organigrama)
        niveles.delete()

        #CREACION DE NIVELES Y VALIDACION DEL ORDEN DE NIVEL
        contador = 1
        for nivel in data:
            id_nivel = nivel.get('id_nivel_organigrama')
            orden_nivel = nivel.get('orden_nivel')
            
            if orden_nivel == contador:
                contador += 1
                pass
            else:
                return Response({'success': False, 'detail': 'No coincide el orden de los niveles'}, status=status.HTTP_400_BAD_REQUEST)
            
            nivel_instance = NivelesOrganigrama.objects.filter(id_nivel_organigrama=id_nivel).first()
            nivel_serializer = self.serializer_class(nivel_instance, data=nivel)
            nivel_serializer.is_valid(raise_exception=True)
            nivel_serializer.save()

        return Response({'success':True,'detail': 'Actualizacion exitosa de los niveles'}, status=status.HTTP_201_CREATED)

class GetNiveles(generics.ListAPIView):
    serializer_class = NivelesGetSerializer

    def get(self, request):
        consulta = request.query_params.get('pk')
        if consulta == None:
            niveles = NivelesOrganigrama.objects.all().values()
            if len(niveles) == 0:
                return Response({'success': False, 'detail' : 'Aún no hay niveles registrados'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'success': True, 'Niveles' : niveles}, status=status.HTTP_200_OK)
        else:
            nivel = NivelesOrganigrama.objects.filter(id_nivel_organigrama=int(consulta)).values()
            return Response({'success': True, 'Nivel': nivel}, status=status.HTTP_200_OK)
    
    
class CreateUnidades(generics.CreateAPIView):
    serializer_class = UnidadesPutSerializer
    queryset = UnidadesOrganizacionales.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data, many=True)
        try:
            serializer.is_valid(raise_exception=True)
            pass
        except:
            return Response({'success': False, 'detail': 'Valide los datos ingresados'}, status=status.HTTP_400_BAD_REQUEST)  
        try:
            serializer.save()
            pass
        except:
            return Response({'success': False, 'detail': 'No se pudo guardar las unidades'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': True, 'detail': serializer.data}, status=status.HTTP_201_CREATED)
    
class UpdateUnidades(generics.UpdateAPIView):
    serializer_class=UnidadesPutSerializer
    queryset=UnidadesOrganizacionales.objects.all()

    def put(self, request, pk):
        data = request.data
        organigrama=Organigramas.objects.filter(id_organigrama=pk).first()
        if organigrama:
            if data:
                nivel_unidades = sorted(data, key=itemgetter('id_nivel_organigrama'))
                
                # ELIMINACION DE UNIDADES
                unidades_eliminar = UnidadesOrganizacionales.objects.filter(id_organigrama=pk)
                unidades_eliminar.delete()
                
                # VALIDACIONES
                
                # VALIDACIÓN DE EXISTENCIA DE NIVELES
                niveles_list = [unidad['id_nivel_organigrama'] for unidad in data]
                niveles_existe = NivelesOrganigrama.objects.filter(id_nivel_organigrama__in=niveles_list)
                if niveles_existe.count() != len(list(dict.fromkeys(niveles_list))):
                    return Response({'success':False, 'detail':'Uno o varios niveles que está asociando no existen'}, status=status.HTTP_400_BAD_REQUEST)
                
                # VALIDACIÓN DE UNA SOLA RAÍZ
                raiz_list = [unidad['unidad_raiz'] for unidad in data]
                if raiz_list.count(True) > 1:
                    return Response({'success':False, 'detail':'No puede definir más de una unidad como raíz'}, status=status.HTTP_400_BAD_REQUEST)
                
                # VALIDACIÓN DE EXISTENCIA DE SECCIÓN Y UNA SOLA SECCIÓN
                seccion_list = [unidad['cod_agrupacion_documental'] for unidad in data]
                if seccion_list:
                    if seccion_list.count('SEC') > 1:
                        return Response({'success':False, 'detail':'No puede definir más de una unidad como sección'}, status=status.HTTP_400_BAD_REQUEST)
                    if ('SUB' in seccion_list) and ('SEC' not in seccion_list):
                        return Response({'success':False, 'detail':'Debe definir la sección para las subsecciones'}, status=status.HTTP_400_BAD_REQUEST)           
                
                # VALIDACIÓN DE EXISTENCIA UNIDAD RAÍZ Y PERTENENCIA A NIVEL UNO
                unidad_raiz = list(filter(lambda unidad: unidad['unidad_raiz'] == True, data))
                if unidad_raiz:
                    nivel_instance = NivelesOrganigrama.objects.filter(id_nivel_organigrama=unidad_raiz[0]['id_nivel_organigrama']).first()
                    if nivel_instance.orden_nivel != 1:
                        return Response({'success':False, 'detail':'La unidad raíz solo puede pertenecer al nivel uno'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'success':False, 'detail':'Debe enviar la unidad raíz'}, status=status.HTTP_400_BAD_REQUEST)
                
                # VALIDACIÓN QUE SECCIÓN SEA UNIDAD RAÍZ
                seccion_raiz = list(filter(lambda unidad: unidad['cod_agrupacion_documental'] == 'SEC', data))
                if seccion_raiz:
                    nivel_instance = NivelesOrganigrama.objects.filter(id_nivel_organigrama=seccion_raiz[0]['id_nivel_organigrama']).first()
                    if nivel_instance.orden_nivel != 1:
                        return Response({'success':False, 'detail':'La sección solo puede pertenecer a la unidad del nivel raíz'}, status=status.HTTP_400_BAD_REQUEST)
                
                # VALIDACIÓN QUE UNIDADES STAFF SEAN DE NIVEL DOS
                staff_unidades = list(filter(lambda unidad: unidad['cod_tipo_unidad'] != 'LI', data))
                for unidad in staff_unidades:
                    nivel_instance = NivelesOrganigrama.objects.filter(id_nivel_organigrama=unidad['id_nivel_organigrama']).first()
                    if nivel_instance.orden_nivel != 2:
                        return Response({'success':False, 'detail':'Las unidades de staff solo pueden pertenecer al nivel dos'}, status=status.HTTP_400_BAD_REQUEST)
                        
                # CREACION DE UNIDADES
                for nivel, unidades in groupby(nivel_unidades, itemgetter('id_nivel_organigrama')):
                    nivel_instance = NivelesOrganigrama.objects.filter(id_nivel_organigrama=nivel).first()
                    if nivel_instance:
                        for unidad in unidades:
                            unidad_serializer = self.serializer_class(data=unidad)
                            unidad_serializer.is_valid(raise_exception=True)
                            
                            unidad_org = None
                            
                            if unidad['cod_tipo_unidad'] == 'LI':
                                unidad_org = UnidadesOrganizacionales.objects.filter(codigo=unidad['cod_unidad_org_padre']).first()
                                unidad_org = unidad_org if unidad_org else None
                            
                            UnidadesOrganizacionales.objects.create(
                                id_nivel_organigrama=nivel_instance,
                                nombre=unidad['nombre'],
                                codigo=unidad['codigo'],
                                cod_tipo_unidad=unidad['cod_tipo_unidad'],
                                cod_agrupacion_documental=unidad['cod_agrupacion_documental'],
                                unidad_raiz=unidad['unidad_raiz'],
                                id_organigrama=organigrama,
                                id_unidad_org_padre=unidad_org
                            )
                    else:
                        return Response({'success':False, 'detail':'El nivel con id ' + str(nivel) + ' no existe'}, status=status.HTTP_400_BAD_REQUEST)
                
                return Response({'success':True,'detail': 'Actualizacion exitosa de las unidades'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'success':False, 'detail':'Debe crear por lo menos una unidad'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'success':False, 'detail':'El organigrama no existe'}, status=status.HTTP_404_NOT_FOUND)


class ActivarOrganigrama(generics.UpdateAPIView):
    serializer_class =OrganigramaSerializer
    queryset=Organigramas.objects.all()
    
    def put(self,request,pk):    

        try:
            organigrama_a_remplazar=Organigramas.objects.filter(actual=True).first()
            organigrama_remplazante=Organigramas.objects.filter(id_organigrama=pk).first()
            previous_remplazante=copy.copy(organigrama_remplazante)
            previous_a_remplazar=copy.copy(organigrama_a_remplazar)
            if organigrama_a_remplazar:
                if organigrama_remplazante:
                    organigrama_remplazante.actual=True
                    organigrama_a_remplazar.actual=False
                    organigrama_remplazante.fecha_puesta_produccion=date.today()
                    organigrama_a_remplazar.fecha_retiro_produccion=date.today()
                    organigrama_a_remplazar.save()
                    organigrama_remplazante.save()
                    
                    #auditoria de organigrama activado
                    user_logeado = request.user.id_usuario
                    dirip = Util.get_client_ip(request)
                    descripcion = {"nombre":str(organigrama_remplazante.nombre)}
                    valores_actualizados={'previous':previous_remplazante, 'current':organigrama_remplazante}
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
                    
                    #auditoria de organigrama desactivado
                
                    descripcion = {"nombre":str(organigrama_a_remplazar.nombre)}
                    valores_actualizados={'previous':previous_a_remplazar, 'current':organigrama_a_remplazar}
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
                    
                    return Response({'success':True,'detail': 'Organigrama activado'}, status=status.HTTP_200_OK)
                return Response({'success':False,'detail': 'No existe ningún organigrama con este ID'}, status=status.HTTP_404_NOT_FOUND)
            else:
                #primer organigrama activado
                if organigrama_remplazante:
                    organigrama_remplazante.actual=True
                    organigrama_remplazante.fecha_puesta_produccion=date.today()
                    organigrama_remplazante.save()
                    
                    user_logeado = request.user.id_usuario
                    dirip = Util.get_client_ip(request)
                    descripcion = {"nombre":str(organigrama_remplazante.nombre)}
                    valores_actualizados={'previous':previous_remplazante, 'current':organigrama_remplazante}
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
                    return Response({'success':True,'detail': 'Primer organigrama activado'}, status=status.HTTP_200_OK)
                return Response({'success':False,'detail': 'No existe ningún organigrama con este ID'}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({'success':False,'detail':'Los parametros enviados son incorrecto'},status=status.HTTP_404_NOT_FOUND)

class CreateOrgChart(generics.CreateAPIView):
    serializer_class = OrganigramaSerializer
    queryset = Organigramas.objects.all()
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetOrganigrama(generics.ListAPIView):
    serializer_class = OrganigramaSerializer  

    def get(self, request):
        consulta = request.query_params.get('pk')
        if consulta == None:
            organigramas = Organigramas.objects.all().values()
            if len(organigramas) == 0:
                return Response({'Error' : 'Aún no hay organigramas registrados'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'Organigramas' : organigramas}, status=status.HTTP_200_OK) 
        organigrama = Organigramas.objects.filter(id_organigrama=int(consulta)).values()
        if len(organigrama) == 0:
            return Response({'Error' : 'No se encontró el organigrama ingresado'}, status=status.HTTP_404_NOT_FOUND)
        niveles = NivelesOrganigrama.objects.filter(id_organigrama=int(consulta)).values()
        if len(niveles) == 0:
            niveles = 'No hay niveles registrados'
            unidades = 'No hay unidades registradas'
            datos_finales = {'Organigrama' : organigrama, 'Niveles' : niveles, 'Unidades' : unidades}
            return Response({'Organigrama' : datos_finales}, status=status.HTTP_200_OK)   
        unidades = UnidadesOrganizacionales.objects.filter(id_organigrama=int(consulta)).values()
        if len(unidades) == 0:
            unidades = 'No hay unidades registradas'
            datos_finales = {'Organigrama' : organigrama, 'Niveles' : niveles, 'Unidades' : unidades}
            return Response({'Organigrama' : datos_finales}, status=status.HTTP_200_OK)
        datos_finales = {'Organigrama' : organigrama, 'Niveles' : niveles, 'Unidades' : unidades}
        return Response({'Organigrama' : datos_finales}, status=status.HTTP_200_OK)

class GetUnidades(generics.ListAPIView):
        serializer_class = UnidadesGetSerializer
        queryset = UnidadesOrganizacionales.objects.filter()
           
        def get(self, request):
            consulta = request.query_params.get('pk')
            if consulta == None:
                unidades = UnidadesOrganizacionales.objects.all().values()
                if len(unidades) == 0:
                    return Response({'success': False, 'detail' : 'Aún no hay unidades registradas'}, status=status.HTTP_404_NOT_FOUND)
                return Response({'success': True, 'Unidades' : unidades}, status=status.HTTP_200_OK)
            unidades = UnidadesOrganizacionales.objects.filter(id_unidad_organizacional = int(consulta)).values()
            unidades_vector = unidades[0]
            id_niveles = unidades_vector['id_nivel_organigrama_id']
            nivel = NivelesOrganigrama.objects.filter(id_nivel_organigrama = id_niveles).values()
            unidades_vector['id_nivel_organigrama_id'] = nivel
            return Response({'Unidades' : unidades_vector})