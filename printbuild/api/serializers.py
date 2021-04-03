from rest_framework import serializers
from .models import *


class SpareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spare
        fields = ['spare','status','transNo','id']

class SpareUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spare
        fields = ['spare','status','transNo','id']
        read_only_fields = ['spare','status','transNo','id']