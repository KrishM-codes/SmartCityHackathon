from rest_framework import serializers
from .models import Query
from django.contrib.auth import get_user_model

class QuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Query
        fields = ['id','Title','Description','Location','Posted_by']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = "__all__"

# class QuerySerializer(serializers.Serializer):
#     Title = serializers.CharField(max_length=150)
#     Description = serializers.CharField()
#     Location = serializers.CharField(max_length=200)
#     # Status = serializers.CharField(max_length=3)
#     # Created = serializers.DateTimeField()
#     Posted_by = serializers.CharField()
    
#     def create(self, validated_data):
#         if 'Status' not in validated_data:
#             validated_data['Status'] = Query.PENDING  # or 'PeQ'

#         if 'Created' not in validated_data:
#             validated_data['Created'] = Query._meta.get_field('Created').auto_now_add

#         # Convert Posted_by to a User instance
#         posted_by_username = validated_data.pop('Posted_by')
#         try:
#             user = User.objects.get(username=posted_by_username)
#             validated_data['Posted_by'] = user
#         except User.DoesNotExist:
#             validated_data['Posted_by'] = None  # or handle it differently

#         return Query.objects.create(**validated_data)
    
#     def update(self,instance,validated_data):
#         instance.Title = validated_data.get('Title',instance.Title)
#         instance.Description = validated_data.get('Description',instance.Description)
#         instance.Location = validated_data.get('Location',instance.Location)
#         instance.Posted_by = validated_data.get('Posted_by',instance.Posted_by)
#         instance.save()
#         return instance

