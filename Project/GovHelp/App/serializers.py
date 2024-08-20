from rest_framework import serializers
from .models import Query
from django.contrib.auth import get_user_model

class QuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Query
        fields = ['id','Title','Description','Location','Posted_by']

class QuerygetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Query
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = "__all__"
