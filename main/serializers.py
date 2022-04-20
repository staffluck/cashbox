from rest_framework import serializers

from .models import Item

class ChequeSerializer(serializers.Serializer):
    ids = serializers.PrimaryKeyRelatedField(many=True, queryset=Item.objects.all())
