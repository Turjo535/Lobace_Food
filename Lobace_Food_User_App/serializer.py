from rest_framework import serializers
from .models import CustomUser

class UserSignupSerializer(serializers.ModelSerializer):
    password= serializers.CharField(write_only=True)
    class Meta:
        model=CustomUser
        fields=['first_name','last_name','email','phone','password',]

    def create(self, validated_data):
        password=validated_data.pop('password')
        validated_data['is_active']=False
        user=CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
