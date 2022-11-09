from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from itertools import groupby
from seguridad.utils import Util
from datetime import date
import copy
from operator import itemgetter
from almacen.serializers.organigrama_serializers import NivelesPostSerializer, OrganigramaSerializer, UnidadesPutSerializer, OrganigramaActivateSerializer, NivelesUpdateSerializer
from almacen.models.organigrama_models import (
    Organigramas,
    UnidadesOrganizacionales,
    NivelesOrganigrama
    )

class GetOrganigramas(generics.ListAPIView):
    serializer_class = OrganigramaSerializer

    def get(self, pk):
        organigrama = Organigramas.objects.filter(id_organigrama=pk).first()
        id_organigrama = organigrama['id_organigrama']
        #niveles = 
        return Response({'Organigrama' : organigrama}, status=status.HTTP_200_OK)    


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
        try:
            organigrama = Organigramas.objects.get(id_organigrama=id_organigrama)
            print(organigrama)
            pass
        except:
            return Response({'success': False, 'detail': 'No se pudo encontrar un organigrama con los parámetros ingresados'}, status=status.HTTP_400_BAD_REQUEST)

        if data:
            nivel_list = []
            for nivel in data:
                id_nivel = nivel.get('id_nivel_organigrama')
                if id_nivel:
                    nivel_list.append(id_nivel)
                    nivel_instance = NivelesOrganigrama.objects.filter(id_nivel_organigrama=id_nivel).first()
                    nivel_serializer = self.serializer_class(nivel_instance, data=nivel)
                    nivel_serializer.is_valid(raise_exception=True)
                    nivel_serializer.save()
                else:
                    organigrama = Organigramas.objects.filter(id_organigrama=id_organigrama).first()
                    nivel_creado = NivelesOrganigrama.objects.create(
                        id_organigrama=organigrama,
                        orden_nivel= nivel['orden_nivel'],
                        nombre=nivel['nombre']
                    )
                    nivel_list.append(nivel_creado.id_nivel_organigrama)
            
            # ELIMINACION DE NIVELES
            niveles_eliminar = NivelesOrganigrama.objects.filter(id_organigrama=id_organigrama).exclude(id_nivel_organigrama__in=nivel_list)
            niveles_eliminar.delete()

            return Response({'success':True,'detail': 'Actualizacion exitosa de los niveles'}, status=status.HTTP_201_CREATED)
        else:
            niveles_eliminar = NivelesOrganigrama.objects.filter(id_organigrama=id_organigrama)
            niveles_eliminar.delete()

            return Response({'success':True,'detail': 'Actualizacion exitosa de los niveles'}, status=status.HTTP_201_CREATED)
    
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
        if data:
            nivel_unidades = sorted(data, key=itemgetter('id_nivel_organigrama'))
            unidades_list = []
            for nivel, unidades in groupby(nivel_unidades, itemgetter('id_nivel_organigrama')):
                # CREACION Y ACTUALIZACION DE UNIDADES
                for unidad in unidades:
                    id_unidad = unidad.get('id_unidad_organizacional')
                    if id_unidad:
                        unidades_list.append(id_unidad)
                        unidad_instance = UnidadesOrganizacionales.objects.filter(id_unidad_organizacional=id_unidad).first()
                        unidad_serializer = self.serializer_class(unidad_instance, data=unidad)
                        unidad_serializer.is_valid(raise_exception=True)
                        unidad_serializer.save()
                    else:
                        nivel_instance = NivelesOrganigrama.objects.filter(id_nivel_organigrama=nivel).first()
                        unidad_creada = UnidadesOrganizacionales.objects.create(
                            id_nivel_organigrama=nivel_instance,
                            nombre=unidad['nombre'],
                            codigo=unidad['codigo'],
                            cod_tipo_unidad=unidad['cod_tipo_unidad'],
                            cod_agrupacion_documental=unidad['cod_agrupacion_documental'],
                            unidad_raiz=unidad['unidad_raiz'],
                            id_organigrama=organigrama,
                            id_unidad_org_padre=unidad['id_unidad_org_padre']
                        )
                        unidades_list.append(unidad_creada.id_unidad_organizacional)
                
            # ELIMINACION DE UNIDADES
            unidades_eliminar = UnidadesOrganizacionales.objects.filter(id_organigrama=pk).exclude(id_unidad_organizacional__in=unidades_list)
            unidades_eliminar.delete()

            return Response({'success':True,'detail': 'Actualizacion exitosa de las unidades'}, status=status.HTTP_201_CREATED)
        else:
            unidades_organigrama = UnidadesOrganizacionales.objects.filter(id_organigrama=pk)
            unidades_organigrama.delete()

            return Response({'success':True,'detail': 'Actualizacion exitosa de las unidades'}, status=status.HTTP_201_CREATED)


class ActivarOrganigrama(generics.UpdateAPIView):
    serializer_class = OrganigramaActivateSerializer
    queryset=Organigramas.objects.all()
    
    def put(self,request,pk):

        organigrama_activado=Organigramas.objects.filter(actual=True).first()
        organigrama_desactivado=Organigramas.objects.filter(id_organigrama=pk).first()
        
        if organigrama_activado:
            if organigrama_desactivado:
                desactivado=organigrama_desactivado.actual=True
                activado=organigrama_activado.actual=False
                desactivado.save()
                activado.save()
                return Response("Organigrama activado")
            else:
                return Response(" No hay ningun organigrama con esta id")
        else:
            return Response("No existe ningún organigrama activado")
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