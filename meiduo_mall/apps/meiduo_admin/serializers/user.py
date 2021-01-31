from rest_framework import serializers
from apps.users.models import User

class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','username','mobile','email','password']
        extra_kwargs = {
            'password':{
                'write_only':True,
                'max_length':20,
                'min_length':5
            }
        }
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)