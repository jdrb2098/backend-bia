
from datetime import date, datetime
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.generics import RetrieveUpdateAPIView
from seguridad.models import Auditorias,Personas,Modulos,User
from seguridad.serializers.auditorias_serializers import AuditoriasSerializers,AuditoriasPostSerializers
from rest_framework.response import Response
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import pytz
class UpdateApiViews(RetrieveUpdateAPIView):
    serializer_class=AuditoriasPostSerializers
    queryset = Auditorias.objects.all()
    
class DestroyApiViews(generics.DestroyAPIView):
    serializer_class=AuditoriasSerializers
    queryset = Auditorias.objects.all()

@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def getAuditorias(request):

    #parametros de entrada
    tipo_documento = request.query_params.get('tipo-documento')
    numero_documento = request.query_params.get('numero-documento')
    rango_inicial_fecha = request.query_params.get('rango-inicial-fecha')
    rango_final_fecha = request.query_params.get('rango-final-fecha')
    modulo = request.query_params.get('modulo')
    subsistema = request.query_params.get('subsistema')  
    #validacion de la informacion
    if rango_inicial_fecha==None or rango_final_fecha==None:
        return Response({'success':False, 'message':'No se ingresaron parametros de fecha'})
    if tipo_documento == None:
        tipo_documento = ''
    if numero_documento == None:
        numero_documento = ''
    if modulo == None:
        modulo = 0
    if subsistema == None:
        subsistema = '' 
    # formateando las variables de tipo fecha
    start_date=datetime(int(rango_inicial_fecha.split('-')[2]),int(rango_inicial_fecha.split('-')[1]),int(rango_inicial_fecha.split('-')[0]), tzinfo=pytz.timezone('America/Bogota'))
    end_date=datetime(int(rango_final_fecha.split('-')[2]),int(rango_final_fecha.split('-')[1]),int(rango_final_fecha.split('-')[0]),23,59,59,999, tzinfo=pytz.timezone('America/Bogota'))
    print("parametros de entrada:" + "TD: " + tipo_documento + " ND: " + numero_documento + " FI: " + rango_inicial_fecha + " FF: " + rango_final_fecha, " sub: " + subsistema + " Mod: " + str(modulo))
    def consultaPersona(tipo_documento,numero_documento):
        try:
            auditoria_persona_id = Personas.objects.get(Q(tipo_documento = tipo_documento) & Q(numero_documento=numero_documento)).id_persona
            auditoria_usuario_id = User.objects.get(persona=auditoria_persona_id)
            return auditoria_usuario_id.id_usuario
        except:
            raise TypeError('bad type')
    def consultarModulo(modulo):
        try:
            modulo = Modulos.objects.get(id_modulo=modulo)
            return modulo.id_modulo
        except:
            raise TypeError('bad type')
    def consultarSubsistema(subsistema):
        try:
            subsistema = Modulos.objects.get(subsistema=subsistema)
            return subsistema.subsistema
        except:
            raise TypeError('bad type')
    def consultaAuditoria():
        return Response({"Mensaje":"Buscando"})

    try:
        id_usuario = consultaPersona(tipo_documento,numero_documento)
        print(id_usuario)
        try:
            consultarModulo(modulo)
            try:
                consultarSubsistema(subsistema)
                try:
                    auditorias = Auditorias.objects.filter(fecha_accion__range=[start_date,end_date]).filter(id_usuario=id_usuario).filter(id_modulo = modulo).filter(subsistema = subsistema)
                    page = request.query_params.get('page')
                    paginator = Paginator(auditorias, 10)
                    try:
                        auditorias = paginator.page(page)
                    except PageNotAnInteger:
                        auditorias = paginator.page(1)
                    except EmptyPage:
                        auditorias = paginator.page(paginator.num_pages)
                    if page == None:
                        page = 1
                    page = int(page)
                    serializador = AuditoriasSerializers(auditorias, many=True)
                    if len(auditorias) == 0:
                        return Response({'success':False, 'Message':"No se encontraron coincidencias con los parametros de busqueda"})
                    return Response({"auditorias" : serializador.data, "page" : page, "pages" : paginator.num_pages})
                except:
                    return Response ({"Error" : "Error de auditoria"})
            except:
                #Poner persona, modulo y fecha
                auditorias = Auditorias.objects.filter(fecha_accion__range=[start_date,end_date]).filter(id_usuario=id_usuario).filter(id_modulo = modulo)
                page = request.query_params.get('page')
                paginator = Paginator(auditorias, 10)
                try:
                    auditorias = paginator.page(page)
                except PageNotAnInteger:
                    auditorias = paginator.page(1)
                except EmptyPage:
                    auditorias = paginator.page(paginator.num_pages)
                if page == None:
                    page = 1
                page = int(page)
                serializador = AuditoriasSerializers(auditorias, many=True)
                if len(auditorias) == 0:
                    return Response({'success':False, 'Message':"No se encontraron coincidencias con los parametros de busqueda"})
                return Response({"auditorias" : serializador.data, "page" : page, "pages" : paginator.num_pages})
        except:
            try:
                consultarSubsistema(subsistema)
                auditorias = Auditorias.objects.filter(fecha_accion__range=[start_date,end_date]).filter(id_usuario=id_usuario).filter(subsistema = subsistema)                
                page = request.query_params.get('page')
                paginator = Paginator(auditorias, 10)
                try:
                    auditorias = paginator.page(page)
                except PageNotAnInteger:
                    auditorias = paginator.page(1)
                except EmptyPage:
                    auditorias = paginator.page(paginator.num_pages)
                if page == None:
                    page = 1
                page = int(page)
                serializador = AuditoriasSerializers(auditorias, many=True)

                if len(auditorias) == 0:
                    return Response({'success':False, 'Message':"No se encontraron coincidencias con los parametros de busqueda"})
                return Response({"auditorias" : serializador.data, "page" : page, "pages" : paginator.num_pages})
                #Poner persona, subsistema y fecha
            except:
                #Poner persona y fecha
                auditorias = Auditorias.objects.filter(fecha_accion__range=[start_date,end_date]).filter(id_usuario=id_usuario)
                page = request.query_params.get('page')
                paginator = Paginator(auditorias, 10)
                try:
                    auditorias = paginator.page(page)
                except PageNotAnInteger:
                    auditorias = paginator.page(1)
                except EmptyPage:
                    auditorias = paginator.page(paginator.num_pages)
                if page == None:
                    page = 1
                page = int(page)
                serializador = AuditoriasSerializers(auditorias, many=True)
                if len(auditorias) == 0:
                    return Response({'success':False, 'Message':"No se encontraron coincidencias con los parametros de busqueda"})
                return Response({"auditorias" : serializador.data, "page" : page, "pages" : paginator.num_pages})
    except:
        try:
            consultarModulo(modulo)
            try:
                consultarSubsistema(subsistema)
                #Poner subsistema, modulo y fecha
                auditorias = Auditorias.objects.filter(fecha_accion__range=[start_date,end_date]).filter(id_modulo = modulo).filter(subsistema = subsistema)
                page = request.query_params.get('page')
                paginator = Paginator(auditorias, 10)
                try:
                    auditorias = paginator.page(page)
                except PageNotAnInteger:
                    auditorias = paginator.page(1)
                except EmptyPage:
                    auditorias = paginator.page(paginator.num_pages)
                if page == None:
                    page = 1
                page = int(page)
                serializador = AuditoriasSerializers(auditorias, many=True)
                if len(auditorias) == 0:
                    return Response({'success':False, 'Message':"No se encontraron coincidencias con los parametros de busqueda"})
                return Response({"auditorias" : serializador.data, "page" : page, "pages" : paginator.num_pages})
            except:
                #Poner modulo y fecha
                auditorias = Auditorias.objects.filter(fecha_accion__range=[start_date,end_date]).filter(id_modulo = modulo)                
                page = request.query_params.get('page')
                paginator = Paginator(auditorias, 10)
                try:
                    auditorias = paginator.page(page)
                except PageNotAnInteger:
                    auditorias = paginator.page(1)
                except EmptyPage:
                    auditorias = paginator.page(paginator.num_pages)
                if page == None:
                    page = 1
                page = int(page)
                serializador = AuditoriasSerializers(auditorias, many=True)
                if len(auditorias) == 0:
                    return Response({'success':False, 'Message':"No se encontraron coincidencias con los parametros de busqueda"})
                return Response({"auditorias" : serializador.data, "page" : page, "pages" : paginator.num_pages})
        except:
            try:
                consultarSubsistema(subsistema)
                #Poner subsistema y fecha
                auditorias = Auditorias.objects.filter(fecha_accion__range=[start_date,end_date]).filter(subsistema = subsistema)
                page = request.query_params.get('page')
                paginator = Paginator(auditorias, 10)
                try:
                    auditorias = paginator.page(page)
                except PageNotAnInteger:
                    auditorias = paginator.page(1)
                except EmptyPage:
                    auditorias = paginator.page(paginator.num_pages)
                if page == None:
                    page = 1
                serializador = AuditoriasSerializers(auditorias, many=True)
                if len(auditorias) == 0:
                    return Response({'success':False, 'Message':"No se encontraron coincidencias con los parametros de busqueda"})
                return Response({"auditorias" : serializador.data, "page" : page, "pages" : paginator.num_pages})
            except:
                #Poner fecha
                auditorias = Auditorias.objects.filter(fecha_accion__range=[start_date,end_date])
                page = request.query_params.get('page')
                paginator = Paginator(auditorias, 10)
                try:
                    auditorias = paginator.page(page)
                except PageNotAnInteger:
                    auditorias = paginator.page(1)
                except EmptyPage:
                    auditorias = paginator.page(paginator.num_pages)
                if page == None:
                    page = 1
                page = int(page)
                serializador = AuditoriasSerializers(auditorias, many=True)
                if len(auditorias) == 0:
                    return Response({'success':False, 'Message':"No se encontraron coincidencias con los parametros de busqueda"})
                return Response({"auditorias" : serializador.data, "page" : page, "pages" : paginator.num_pages}) 

 
   
    
class ListApiViews(generics.ListAPIView):
    serializer_class=AuditoriasSerializers
    queryset = Auditorias.objects.all()

class RegisterApiViews(generics.CreateAPIView):
    queryset = Auditorias.objects.all()
    serializer_class = AuditoriasPostSerializers
    




