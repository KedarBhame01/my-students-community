from rest_framework import serializers
from .models import Admins

class Admins_serializer(serializers.ModelSerializer):
    class Meta:
        model = Admins
        fields = '__all__'
    
class Admins_login_serializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

# class Admins_search_serializer(serializers.Serializer):   
#     search_term = serializers.CharField(required=True)
#     search_in = serializers.ChoiceField(
#         choices=['email']
#     )
    