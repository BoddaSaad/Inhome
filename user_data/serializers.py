from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email as django_validate_email
from .models import *
from .models import OrderFile  # Explicit import to ensure OrderFile is available
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.db.models import Avg
User = get_user_model()
from rest_framework.exceptions import ValidationError
from .utils import get_address_from_coordinates

class SingUpSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    username = serializers.CharField(validators=[])
    fcm = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    

    class Meta:
        model = Cuser
        fields = [ 'username', 'email', 'password', 'password2', 'phone', 'Provides_services', 'request_services' ,'latitude','longitude', 'fcm']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Passwords do not match")
        #validate_password(attrs['password'])
        return attrs

    def validate_email(self, value):
        value=value.lower()
        if Cuser.objects.filter(email=value).exists():
            raise serializers.ValidationError('This email is already in use')
        return value



    def create(self, validated_data):
        validated_data.pop('password2')
        fcm = validated_data.get('fcm', None)
        address = get_address_from_coordinates(validated_data['latitude'], validated_data['longitude'])

        user = Cuser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            latitude=validated_data['latitude'],
            longitude=validated_data['longitude'],
            request_services=validated_data['request_services'],
            Provides_services=validated_data['Provides_services'],
            is_active=not validated_data['Provides_services'],
            fcm=fcm,
            password=make_password(validated_data['password']),
            country=address.raw['address']['country'],
            location=address.address
        )
        return user
    
    
        
    def to_representation(self, instance):
        # إصدار التوكين
        refresh = RefreshToken.for_user(instance)
        data = super().to_representation(instance)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data

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
    service_name = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model=Order_service
        fields='__all__'
    def get_service_name(self, obj):
        request = self.context.get('request')
        if request and request.user.lan == 'E': 
            return obj.service.name_english
        else:
            return obj.service.name
        

    def get_name(self, obj):
        return obj.user.username  


class OrderFileSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderFile model to handle multiple file uploads
    """
    class Meta:
        model = OrderFile
        fields = ['id', 'file', 'file_type', 'uploaded_at', 'description']
        read_only_fields = ['id', 'file_type', 'uploaded_at']


class OrderFileCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating OrderFile instances
    """
    class Meta:
        model = OrderFile
        fields = ['file', 'description']


class Order_serviceserlizer_with_files(serializers.ModelSerializer):
    """
    Extended Order service serializer that includes files
    """
    service_name = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    files = OrderFileSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order_service
        fields = '__all__'
    
    def get_service_name(self, obj):
        request = self.context.get('request')
        if request and request.user.lan == 'E': 
            return obj.service.name_english
        else:
            return obj.service.name
        
    def get_name(self, obj):
        return obj.user.username


class CombinedCuserSerializer(serializers.ModelSerializer):
   

    class Meta:
        model = Cuser
        fields = ['country', 'lan', 'phone','location','username']
        

    #def validate(self, attrs):
        #user = self.context.get('request').user  # الحصول على المستخدم الحالي من السياق
        #phone = attrs.get('phone')
        #new_phone = attrs.get('new_phone')

        #if phone and new_phone and phone == new_phone:
         #   raise serializers.ValidationError({"error": "Phone and new phone cannot be the same."})

        #if new_phone and user.phone != new_phone:
           # raise serializers.ValidationError({"error": "New phone number does not match the current phone number in the database."})

        #return attrs


class ServiceProviderOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProviderOffer
        fields = ['order', 'provider', 'price', 'comment', 'created_at']
        read_only_fields = ['created_at']

class ServiceProviderOfferSerializer_put(serializers.ModelSerializer):
    class Meta:
        model = ServiceProviderOffer
        fields = ['order', 'provider', 'price', 'time_arrive', 'created_at','status']
        read_only_fields = ['created_at']







class OfferPriceSerializer(serializers.ModelSerializer):
    provider_name = serializers.SerializerMethodField()
    provider_pic = serializers.SerializerMethodField()
    service_name = serializers.SerializerMethodField()
    email=serializers.SerializerMethodField()
    phone=serializers.SerializerMethodField()
    id_provider=serializers.SerializerMethodField()
    rating=serializers.SerializerMethodField()

    class Meta:
        model = ServiceProviderOffer
        fields = fields = ['id', 'provider_name', 'provider_pic', 'time_arrive', 'price', 'comment', 'created_at', 'status', 'order', 'provider', 'service_name','email','phone','id_provider','rating']
        
    def get_id_provider(slef,obj):
        id=obj.provider.id
        return id 
    

    def get_provider_name(self, obj):
        try:
            brovide_service = Brovides_services.objects.get(user=obj.provider)
            return brovide_service.user.username
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
        
    def get_service_name(self, obj):
        # try:
        #     brovide_service = Brovides_services.objects.get(user=obj.provider)
        #     if getattr(obj.provider,'lan',None)=='A':
        #         return brovide_service.service.name
        #     else:
        #         return brovide_service.service.name_english
        # except Brovides_services.DoesNotExist:
        #     return None
        
        try:
            brovide_service = Brovides_services.objects.get(user=obj.provider)
            request=self.context.get('request')
            user=request.user
            user=Cuser.objects.get(id=user.id)
            if getattr(user,'lan',None)=='A':
                return brovide_service.service.name
            else:
                return brovide_service.service.name_english
        except Brovides_services.DoesNotExist:
            return None
        

            
            
            
        
    def get_phone(self,obj):
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
    
    def get_rating(self, obj):
        user_id = obj.provider.id
        rate = Rating.objects.filter(service_provider__user__id=user_id).aggregate(average=Avg('rating'))
        return rate['average'] or 3


        







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
        fields = ['id','order', 'status', 'order_details']

    def get_order_details(self, obj):
        request=self.context.get('request')
        order = obj.order
        user_language = getattr(request.user, 'lan', None)
        if user_language=='E':
            name_service=order.service.name_english
        else:
            name_service =order.service.name 
        # Get all files for this order
        files = order.files.all()
        files_data = []
        if files:
            files_data = [{
                'id': f.id,
                'url': f.file.url,
                'type': f.file_type,
                'description': f.description,
                'uploaded_at': f.uploaded_at
            } for f in files]
        
        return {
            "service": name_service,
            "user": order.user.username,
            "id_user":order.user.id,
            "type_service": order.type_service,
            "time": order.time,
            "location": order.location,
            "files": files_data,  # Changed from single file to files list
            "count": order.count,
            "id_order":order.id,
            "phone":order.user.phone,
            "latitude":order.latitude,
            "longitude":order.longitude
        }
        




class ServiceProviderOfferUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProviderOffer
        fields = ['price', 'status']
        read_only_fields = ['status']

    def update(self, instance, validated_data):
        instance.price = validated_data.get('price', instance.price)
        instance.status = 'P'  # تغيير الحالة إلى "Pending"
        instance.save()
        return instance
    
    
    
class OfferUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProviderOffer
        fields = ['price', 'status', 'comment']  # الحقول التي يمكن تحديثها



class Noticationserlizer(serializers.ModelSerializer):
    
    title = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    
    class Meta:
        model=Notfications_Broviders
        fields = ['id', 'title', 'content', 'id_offer','brovider']
        
    
    def get_title(self, obj):
        request = self.context.get('request')
        if request and request.user.lan == 'E': 
            return obj.title_english
        return obj.title

    def get_content(self, obj):
        request = self.context.get('request')
        if request and request.user.lan == 'E':
            return obj.content_english
        return obj.content
        
        
class NotificationSerializer_clent(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    class Meta:
        model = notfications_client
        fields = ['id', 'title', 'content', 'user']
        
    def get_title(self, obj):
        request = self.context.get('request')
        if request and request.user.lan == 'E':  
            return obj.title_english
        return obj.title

    def get_content(self, obj):
        request = self.context.get('request')
        if request and request.user.lan == 'E':
            return obj.content_english
        return obj.content
        
    
        
        
class CompleatService(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    service = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    provider=serializers.SerializerMethodField()
    image=serializers.SerializerMethodField()
    files=serializers.SerializerMethodField()  # Add files field
    id_provider=serializers.SerializerMethodField()
    user=serializers.SerializerMethodField()
    rating_cilent=serializers.SerializerMethodField()
    rating_provider=serializers.SerializerMethodField()
    
    class Meta:
        model = ServiceProviderOffer  # Corrected from 'models'
        fields = '__all__'


    def get_user(self,obj):
        return obj.order.user.id
    
    
    def get_id_provider(self,obj):
        return obj.provider.id
    
    def get_image(self,obj):
        # Return the first image file or None
        files = obj.order.files.filter(file_type='image').first()
        if files:
            return files.file.url
        # If no image, return first file of any type
        first_file = obj.order.files.first()
        return first_file.file.url if first_file else None
    
    def get_files(self,obj):
        # Return all files for this order
        files = obj.order.files.all()
        return [{
            'id': f.id,
            'url': f.file.url,
            'type': f.file_type,
            'description': f.description,
            'uploaded_at': f.uploaded_at
        } for f in files]
    
    def get_provider(self,obj):
        return obj.provider.username
    
    def get_name(self, obj):
        client = obj.order.user.username
        return client

    def get_location(self, obj):
        location = obj.order.user.location  # Fixed typo: 'loction' to 'location'
        return location

    def get_price(self, obj):
        price = obj.price
        return price

    def get_service(self, obj):
        
        order = obj.order
        user_language = getattr(order.user, 'lan', 'A')
        if user_language=='A':
            name_service=order.service.name
        else:
            name_service =order.service.name_english 
    
        service = name_service  
        return service

    def get_created_at(self, obj):
        return obj.created_at
    
        
    def get_rating_cilent(self, obj):
        user_id = obj.order.user.id
        rate = ClientRating.objects.filter(client__id=user_id).aggregate(average=Avg('rating'))
        return rate['average'] or 3  # إذا لم تكن هناك تقييمات، يرجع 0

    def get_rating_provider(self, obj):
        user_id = obj.provider.id
        rate = Rating.objects.filter(service_provider__user__id=user_id).aggregate(average=Avg('rating'))
        return rate['average'] or 3
        
# class CompleatServiceWithProvider(CompleatService):
#     provider_name = serializers.SerializerMethodField()

#     class Meta(CompleatService.Meta):
#         fields = CompleatService.Meta.fields + ['provider_name']  # إضافة الحقل الجديد إلى القائمة

#     def get_provider_name(self, obj):
#         return obj.provider.username  # استخراج اسم مقدم الخدمة




class CompleatService_client(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    service = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    pic = serializers.SerializerMethodField()

    class Meta:
        model = ServiceProviderOffer
        fields = ['name', 'price', 'service', 'created_at', 'pic']  # تحديد الحقول التي تحتاجها فقط

    def get_name(self, obj):
        # إرجاع اسم مزود الخدمة بدلاً من الكائن نفسه
        return obj.provider.username  # أو أي حقل تراه مناسباً لاسم مزود الخدمة

    def get_pic(self, obj):
        try:
            # احصل على نموذج Brovides_services بناءً على مزود الخدمة
            brovides_services = Brovides_services.objects.get(user=obj.provider)
            return brovides_services.personlity_pic.url  # إرجاع URL الصورة
        except Brovides_services.DoesNotExist:
            return None

    def get_price(self, obj):
        return obj.price

    def get_service(self, obj):
        return obj.order.service.name  # إرجاع اسم الخدمة

    def get_created_at(self, obj):
        return obj.created_at
    
    
class Offers(serializers.ModelSerializer):
    class Meta:
        model=ServiceProviderOffer
        fields='__all__'
        
        
        
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # إضافة معلومات إضافية إلى التوكن
        token['username'] = user.username
        token['email'] = user.email

        return token

    def validate(self, attrs):
        if 'email' in attrs:
            attrs['email'] = attrs['email'].lower()
        data = super().validate(attrs)
        
        # إرجاع بيانات إضافية مع الاستجابة
        data.update({
            'user_id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            # أضف أي بيانات أخرى تحتاجها
            'provider':self.user.Provides_services,
            'request_user':self.user.request_services,
            
        })

        return data



class Services_selizer(serializers.ModelSerializer):
    
    class Meta:
        model=Services
        fields=['id','name']
        
        
        