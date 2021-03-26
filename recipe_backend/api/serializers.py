from rest_framework import serializers
from .models import *


class ChefUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChefUser
        fields = ('email', 'first_name', 'last_name', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def validate(self, attrs):
        email = attrs.get('email', '')
        if ChefUser.objects.filter(email=email).exists():
            return serializers.ValidationError({'email', ('Este e-mail já existe')})
        return super().validate(attrs)


class RecipeSerializer(serializers.ModelSerializer):
    chef = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'
