from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

class UserRegistrationSerializer (serializers.ModelSerializer):
    password=serializers.CharField(max_length=68,min_length=6, write_only=True)
    password2=serializers.CharField(max_length=68,min_length=6, write_only=True)

    class Meta:
        model=User
        fields=['email','first_name',"last_name",'password','password2']
        extra_kwargs={
            'email':{'required':True},
            'first_name':{'required':True},
            'last_name':{'required':True}
        }

    
    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.pop('password2',None)

        if password!=password2:
            raise serializers.ValidationError({
                'password':'passwords must match.'
            })
        return attrs
    
    def create(self,validated_data):
        try:
            user = User.objects.create(
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                password=make_password(validated_data['password'])
            )
            return user
        except Exception as e:
             raise serializers.ValidationError({
                'error': f'Unable to create user: {str(e)}'
            })


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid password")

        attrs['user'] = user
        return attrs
