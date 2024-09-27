from rest_framework import serializers
from .models import *
class HistoricoCriminalSerializer(serializers.ModelSerializer):

    class Meta:
        model = HistoricoCriminal
        fields = '__all__' 

class CidadaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cidadao
        fields = '__all__'

