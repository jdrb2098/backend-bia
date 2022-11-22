from almacen.models.generics_models import Bodegas
from rest_framework import generics, status
from rest_framework.views import APIView
from almacen.serializers.mantenimientos_serializers import (
    SerializerProgramacionMantenimientos,
    SerializerRegistroMantenimientos,
    AnularMantenimientoProgramadoSerializer
    )
from almacen.models.mantenimientos_models import (
    ProgramacionMantenimientos,
    RegistroMantenimientos,
)
from seguridad.models import (
    Personas
)
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db.models import F, Q
from datetime import datetime

class GetMantenimientosProgramadosById(generics.RetrieveAPIView):
    serializer_class=SerializerProgramacionMantenimientos
    queryset=ProgramacionMantenimientos.objects.all()
    
    def get(self, request, pk):
        mantenimiento_programado = ProgramacionMantenimientos.objects.filter(id_programacion_mtto=pk).first()
        if mantenimiento_programado:
            serializador = self.serializer_class(mantenimiento_programado)
            return Response({'success':True, 'detail':serializador.data}, status=status.HTTP_200_OK)
        else:
            return Response({'success':False, 'detail':'No existe ningún mantenimiento programado con el parámetro ingresado'}, status=status.HTTP_404_NOT_FOUND)

class GetMantenimientosProgramadosFiveList(generics.ListAPIView):
    serializer_class=SerializerProgramacionMantenimientos
    queryset=ProgramacionMantenimientos.objects.all()
    
    def get(self, request, id_articulo):
        mantenimientos_programados = ProgramacionMantenimientos.objects.filter(id_articulo=id_articulo, ejecutado=False, fecha_anulacion=None).values(id_programacion_mantenimiento=F('id_programacion_mtto'), tipo=F('cod_tipo_mantenimiento'), fecha=F('fecha_programada')).order_by('fecha')[:5]
        if mantenimientos_programados:
            mantenimientos_programados = [dict(item, estado='Vencido' if item['fecha'] < datetime.now().date() else 'Programado') for item in mantenimientos_programados]
            mantenimientos_programados = [dict(item, responsable='NA') for item in mantenimientos_programados]
            mantenimientos_programados = [dict(item, tipo_descripcion='Correctivo' if item['tipo']=='C' else 'Preventivo') for item in mantenimientos_programados]
            return Response({'status':True, 'detail':mantenimientos_programados}, status=status.HTTP_200_OK)
        else:
            return Response({'success':False, 'detail':'No existe ningún mantenimiento programado para este artículo'}, status=status.HTTP_404_NOT_FOUND)
            
class GetMantenimientosProgramadosList(generics.ListAPIView):
    serializer_class=SerializerProgramacionMantenimientos
    queryset=ProgramacionMantenimientos.objects.all()
    
    def get(self, request, id_articulo):
        mantenimientos_programados = ProgramacionMantenimientos.objects.filter(id_articulo=id_articulo).values(id_programacion_mantenimiento=F('id_programacion_mtto'), tipo=F('cod_tipo_mantenimiento'), fecha=F('fecha_programada')).order_by('fecha')
        if mantenimientos_programados:
            mantenimientos_programados = [dict(item, estado='Vencido' if item['fecha'] < datetime.now().date() else 'Programado') for item in mantenimientos_programados]
            mantenimientos_programados = [dict(item, responsable='NA') for item in mantenimientos_programados]
            mantenimientos_programados = [dict(item, tipo_descripcion='Correctivo' if item['tipo']=='C' else 'Preventivo') for item in mantenimientos_programados]
            return Response({'status':True, 'detail':mantenimientos_programados}, status=status.HTTP_200_OK)
        else:
            return Response({'success':False, 'detail':'No existe ningún mantenimiento programado para este artículo'}, status=status.HTTP_404_NOT_FOUND)


class AnularMantenimientoProgramado(generics.RetrieveUpdateAPIView):
    serializer_class = AnularMantenimientoProgramadoSerializer
    queryset = ProgramacionMantenimientos.objects.all()
    lookup_field = 'id_programacion_mtto'

    def patch(self, request, id_programacion_mtto):
        persona_usuario_logeado = request.user.persona.id_persona
        persona_instance = Personas.objects.filter(id_persona=persona_usuario_logeado).first()
        mantenimiento = ProgramacionMantenimientos.objects.filter(id_programacion_mtto=id_programacion_mtto).first()
        if mantenimiento:
            if mantenimiento.ejecutado == True:
                return Response({'success': False, 'detail': 'No puede anular un mantenimiento que ya fue ejecutado'}, status=status.HTTP_403_FORBIDDEN)
            serializador = self.serializer_class(mantenimiento, data=request.data, many=False)
            serializador.is_valid(raise_exception=True)
            mantenimiento.fecha_anulacion = datetime.now()
            mantenimiento.id_persona_anula = persona_instance
            serializador.save()
            mantenimiento.save()

            return Response({'success': True, 'detail': 'Anulación exitosa'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'success': False, 'detail': 'No existe ningún mantenimiento con el parámetro ingresado'}, status=status.HTTP_404_NOT_FOUND)
        

class GetMantenimientosEjecutadosFiveList(generics.ListAPIView):
    serializer_class=SerializerRegistroMantenimientos
    queryset=RegistroMantenimientos.objects.all()
    
    def get(self, request, id_articulo):
        mantenimientos_completado = RegistroMantenimientos.objects.filter(id_articulo=id_articulo).values(id_registro_mantenimiento=F('id_registro_mtto'), tipo=F('cod_tipo_mantenimiento'), fecha=F('fecha_ejecutado'), responsable=F('id_persona_realiza')).order_by('-fecha')[:5]
        if mantenimientos_completado:
            mantenimientos_completado = [dict(item, estado='Completado') for item in mantenimientos_completado]
            mantenimientos_completado = [dict(item, tipo_descripcion='Correctivo' if item['tipo']=='C' else 'Preventivo') for item in mantenimientos_completado]
            
            for mantenimiento in mantenimientos_completado:
                persona = Personas.objects.filter(id_persona=mantenimiento['responsable']).first()
                mantenimiento['fecha'] = mantenimiento['fecha'].date()
                mantenimiento['responsable'] = persona.primer_nombre + ' ' + persona.primer_apellido if persona.tipo_persona=='N' else persona.razon_social
        else:
            return Response({'success': False, 'detail': 'No existe ningún mantenimiento registrado para este articulo'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'status':True, 'detail':mantenimientos_completado}, status=status.HTTP_200_OK)

class GetMantenimientosEjecutadosList(generics.ListAPIView):
    serializer_class=SerializerRegistroMantenimientos
    queryset=RegistroMantenimientos.objects.all()
    
    def get(self, request, id_articulo):
        mantenimientos_completado = RegistroMantenimientos.objects.filter(id_articulo=id_articulo).values(id_registro_mantenimiento=F('id_registro_mtto'), tipo=F('cod_tipo_mantenimiento'), fecha=F('fecha_ejecutado'), responsable=F('id_persona_realiza')).order_by('-fecha')
        if mantenimientos_completado: 
            mantenimientos_completado = [dict(item, estado='Completado') for item in mantenimientos_completado]
            mantenimientos_completado = [dict(item, tipo_descripcion='Correctivo' if item['tipo']=='C' else 'Preventivo') for item in mantenimientos_completado]
            
            for mantenimiento in mantenimientos_completado:
                persona = Personas.objects.filter(id_persona=mantenimiento['responsable']).first()
                mantenimiento['fecha'] = mantenimiento['fecha'].date()
                mantenimiento['responsable'] = persona.primer_nombre + ' ' + persona.primer_apellido if persona.tipo_persona=='N' else persona.razon_social
        else:
            return Response({'success': False, 'detail': 'No existe ningún mantenimiento registrado para este articulo'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'status':True, 'detail':mantenimientos_completado}, status=status.HTTP_200_OK)

class GetMantenimientosEjecutadosById(generics.ListAPIView):
    serializer_class=SerializerRegistroMantenimientos
    queryset=RegistroMantenimientos.objects.all()
    
    def get(self, request, pk):
        mantenimiento_completado = RegistroMantenimientos.objects.filter(id_registro_mtto=pk).first()
        if mantenimiento_completado:
            serializador = self.serializer_class(mantenimiento_completado)
            return Response({'success':True, 'detail':serializador.data}, status=status.HTTP_200_OK)
        else:
            return Response({'success':False, 'detail':'No existe ningún mantenimiento con el parámetro ingresado'}, status=status.HTTP_404_NOT_FOUND)