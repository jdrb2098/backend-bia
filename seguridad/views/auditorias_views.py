from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.generics import RetrieveUpdateAPIView
from seguridad.models import Auditorias
from seguridad.serializers.auditorias_serializers import AuditoriasSerializers,AuditoriasPostSerializers

class UpdateApiViews(RetrieveUpdateAPIView):
    serializer_class=AuditoriasPostSerializers
    queryset = Auditorias.objects.all()
    
class DestroyApiViews(generics.DestroyAPIView):
    serializer_class=AuditoriasSerializers
    queryset = Auditorias.objects.all()
    
class ConsultarApiViews(generics.RetrieveAPIView):
    serializer_class=AuditoriasSerializers
    queryset = Auditorias.objects.all()

class ListApiViews(generics.ListAPIView):
    serializer_class=AuditoriasSerializers
    queryset = Auditorias.objects.all()

class RegisterApiViews(generics.CreateAPIView):
    queryset = Auditorias.objects.all()
    serializer_class = AuditoriasPostSerializers
    




