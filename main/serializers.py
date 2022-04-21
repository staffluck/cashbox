from rest_framework import serializers

from .models import Item

class ChequeIdsSerializer(serializers.Serializer):
    items = serializers.PrimaryKeyRelatedField(many=True, queryset=Item.objects.all())
