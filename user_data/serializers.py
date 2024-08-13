from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email as django_validate_email
from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework.exceptions import ValidationError

class SingUpSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Cuser
        fields = ['firs_name', 'email', 'password', 'password2', 'phone', 'Provides_services', 'request_services']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Passwords do not match")
        validate_password(attrs['password'])
        return attrs

    def validate_email(self, value):
        if Cuser.objects.filter(email=value).exists():
            raise serializers.ValidationError('This email is already in use')
        django_validate_email(value)
        return value

    def create(self, validated_data):
        validated_data.pop('password2')
        user = Cuser.objects.create(
            firs_name=validated_data['firs_name'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            Provides_services=validated_data['Provides_services'],
            request_services=validated_data['request_services'],
            password=make_password(validated_data['password']),
        )
        return user


class Brovice_data(serializers.ModelSerializer):
    class Meta:
        model= Brovides_services
        fields='__all__'


class ResetPasswordSerializer(serializers.Serializer):
    email=serializers.EmailField()
    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError("This email does not exist")
        return attrs


class CheckCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)


class Change_password(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(max_length=100, min_length=8)
    password2=serializers.CharField(max_length=100, min_length=8)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        password2 = attrs.get('password2')

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "User with this email does not exist"})

        if password != password2:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        
        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        
        return attrs
    


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    def get_client_average_rating(self, obj):
        ratings = ClientRating.objects.filter(client=obj)
        if ratings.exists():
            return ratings.aggregate(models.Avg('rating'))['rating__avg']
        return 0

        



class Serviceserleszer(serializers.ModelSerializer):
    class Meta:
        model=Services
        fields='__all__'
        


class Order_serviceserlizer(serializers.ModelSerializer):
    class Meta:
        model=Order_service
        fields='__all__'



class CuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuser
        fields = [  'country', 'lan',  ]


class CuserSerializer_2(serializers.ModelSerializer):
    class Meta:
        model = Cuser
        fields = ['name','phone','new_phone', 'location']

    def validate(self, attrs):
        phone=attrs['phone']
        new_phone=attrs['new_phone']
        if phone == new_phone:
            raise serializers.ValidationError({"eroor":"same number "})




class ServiceProviderOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProviderOffer
        fields = ['order', 'provider', 'price', 'comment', 'created_at']
        read_only_fields = ['created_at']



class OfferPriceSerializer(serializers.ModelSerializer):
    provider_name = serializers.SerializerMethodField()
    provider_pic = serializers.SerializerMethodField()

    class Meta:
        model = ServiceProviderOffer
        fields = '__all__'

    def get_provider_name(self, obj):
        try:
            brovide_service = Brovides_services.objects.get(user=obj.provider)
            return brovide_service.user.first_name
        except Brovides_services.DoesNotExist:
            return None

    def get_provider_pic(self, obj):
        try:
            brovide_service = Brovides_services.objects.get(user=obj.provider)
            if brovide_service.personlity_pic:
                return brovide_service.personlity_pic.url
            return None
        except Brovides_services.DoesNotExist:
            return None
        
    def get_name_service(self,obj):
        try:
            brovide_service = Brovides_services.objects.get(user=obj.provider)
            return brovide_service.service
        except Brovides_services.DoesNotExist:
            return None
        
    def get_phone_number(self,obj):
        try:
            brovide_service = Brovides_services.objects.get(user=obj.provider)
            return brovide_service.user.phone
        except Brovides_services.DoesNotExist:
            return None
        
    def get_email(self,obj):
        try:
            brovide_service = Brovides_services.objects.get(user=obj.provider)
            return brovide_service.user.email
        except Brovides_services.DoesNotExist:
            return None
        
    def get_average_rating(self, obj):
        return obj.rating

        

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['service_provider', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['user']

    def create(self, validated_data):
        rating = Rating.objects.create(**validated_data)
        # تحديث متوسط التقييم لمقدم الخدمة
        rating.service_provider.update_rating()
        return rating
    

class ClientRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientRating
        fields = '__all__'



class GET_orders(serializers.ModelSerializer):
    order_details = serializers.SerializerMethodField()

    class Meta:
        model = ServiceProviderOffer
        fields = ['order', 'status', 'order_details']

    def get_order_details(self, obj):
        order = obj.order
        return {
            "service": order.service.name,
            "user": order.user.first_name,
            "type_service": order.type_service,
            "time": order.time,
            "location": order.location,
            "file": order.file.url,
            
            "count": order.count
        }
