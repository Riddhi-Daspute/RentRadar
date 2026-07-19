from rest_framework import serializers
from .classes import Property


class PropertySerializer(serializers.Serializer):

    property_id = serializers.CharField()
    title = serializers.CharField()
    owner = serializers.CharField()
    phone = serializers.CharField()
    area = serializers.CharField()
    city = serializers.CharField()
    pincode = serializers.CharField()
    rent = serializers.IntegerField()
    amenities = serializers.CharField()
    price_history = serializers.ListField()