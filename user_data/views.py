from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .serializers import SingUpSerializer
from .models import *
from .serializers import *
import random
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth import get_user_model
User = get_user_model()
class SingViewSet(APIView):
    def post(self, request):
        data = request.data
        serializer = SingUpSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully", "user_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Brovicevieset(APIView):
    def post(self,request):
        try:
            data=request.data 
            serializer=Brovice_data(data=data)
            brovice=serializer.save()
            return Response({"account":"is active now "},status=status.HTTP_200_OK)
        except Exception as e :
            return Response ({"eroor":str(e)},status=status.HTTP_400_BAD_REQUEST)
        




def generate_random_code(length=6):
    code = ''.join(random.choices('0123456789', k=length))
    return code
    
class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)  # الحصول على المستخدم بناءً على البريد الإلكتروني
            code = generate_random_code()  # توليد رمز عشوائي
            cache.set(f'reset_code_{email}', code, timeout=600)
            subject = 'Reset Password'
            message = f'Hi {user.first_name}, your reset code is {code}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            
            send_mail(subject, message, email_from, recipient_list)
            
            return Response({"message": "Reset code sent"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckCodeView(APIView):
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        if not email or not code:
            return Response({"error": "Email and code are required"}, status=status.HTTP_400_BAD_REQUEST)
    
        stored_code = cache.get(f'reset_code_{email}')
        
        if stored_code == code:
            return Response({"message": "Code is valid"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)
        
class Change_passviwe(APIView):
    def post(self,request):
        data=request.data 
        serializer=Change_password(data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(email=email)
                user.set_password(password)  # استخدم set_password لتشفير كلمة المرور
                user.save()
                return Response({"success": "Password change successful"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User with this email does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
        
class Serviceviewset(APIView):
    def get(self, request):
        try:
            service_name = request.query_params.get('name', None)
            
            if service_name:
                service = Services.objects.filter(name__icontains=service_name)
            else:
                service = Services.objects.all()
            serializer = Serviceserleszer(service, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Orderservicevieset(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            service = Services.objects.get(id=id)
            serializer = Serviceserleszer(service)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Services.DoesNotExist:
            return Response({"error": "Service not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, id):
        try:
            service = Services.objects.get(id=id)
            user = request.user

            # نسخ البيانات وتحديث الحقول المطلوبة
            data = request.data.copy()
            data['user'] = user.id
            data['service'] = service.id

            serializer = Order_serviceserlizer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response({"done": "Order created successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Services.DoesNotExist:
            return Response({"error": "Service not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        

class CuserUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        try:
            user = Cuser.objects.get(id=user_id)
        except Cuser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CuserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class CuserUpdateView_2(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        try:
            user = Cuser.objects.get(id=user_id)
        except Cuser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CuserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class Offered_services(APIView):
    permission_classes=[IsAuthenticated]
    def get (slef,reuest):
        try:
            offer=Order_service.objects.all()
            serializer=Order_serviceserlizer(offer,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
        

class detal_service(APIView):
    permission_classes=[IsAuthenticated]
    def get(self ,request,id):
        try:
            service=Order_service.objects.get(id=id)
            serializer=Order_serviceserlizer(service)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
        

    def post(self, request, order_id):
        try:
            order = Order_service.objects.get(id=order_id)
            provider = request.user
            data = request.data
            data['order'] = order.id
            data['provider'] = provider.id

            serializer = ServiceProviderOfferSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, offer_id):
        try:
            offer = ServiceProviderOffer.objects.get(id=offer_id)
            data = request.data
            data['status'] = 'A'  # تعيين الحالة هنا إذا كنت تريد تحديثها دائمًا إلى 'A'
            serializer = ServiceProviderOfferSerializer(offer, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ServiceProviderOffer.DoesNotExist:
            return Response({"error": "Offer not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class All_offers(APIView):
    def get(self,request):
        try:    
            offers = ServiceProviderOffer.objects.all()
            serializer=OfferPriceSerializer(offers,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e :
            return Response({'eroor':str(e)},status=status.HTTP_400_BAD_REQUEST) 
            



class OfferDecisionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, offer_id):
        try:
            offer = ServiceProviderOffer.objects.get(id=offer_id)
            decision = request.data.get('decision')

            if decision == 'accept':
                offer.status = 'A'
                offer.save()
                noteifcation=Notfications_Broviders.objects.create(
                    brovider=offer.provider,
                    title="تم تاكيد طلبك من جانب العميل ",
                    content='انقر للذهاب اللي صفحه الطلبات القادمه ',


                )

                return Response({"message": "Offer accepted."}, status=status.HTTP_200_OK)
            elif decision == 'reject':
                offer.status = 'R'
                offer.save()
                noteifcation=Notfications_Broviders.objects.create(
                    brovider=offer.provider,
                    title="تم رفض السعر من جانب العميل ",
                    content='انقر للذهاب لتحديد سعر جديد ',


                )



                return Response({"message": "Offer rejected."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid decision."}, status=status.HTTP_400_BAD_REQUEST)

        except ServiceProviderOffer.DoesNotExist:
            return Response({"error": "Offer not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)




class AcceptedOffersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            accepted_offers = ServiceProviderOffer.objects.filter(status='A', order__user=request.user)
            serializer = OfferPriceSerializer(accepted_offers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CancelServiceProviderOfferView(APIView):
    permission_classes = [IsAuthenticated]



    def post(self, request, offer_id):
        try:
            offer = ServiceProviderOffer.objects.get(id=offer_id)
            
            if offer.status != 'C':
                offer.status = 'C'
                offer.save()
                noteifcation=Notfications_Broviders.objects.create(
                    brovider=offer.provider,
                    title="تم حذف المعاد القادم",
                    content='انقر للذهاب اللي صفحه الطلبات الملغيه ',


                )
                return Response({"message": "Offer canceled."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Offer is already canceled."}, status=status.HTTP_400_BAD_REQUEST)

        except ServiceProviderOffer.DoesNotExist:
              return Response({"error": "Offer not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class Get_canceled_offer(APIView):
    def get(slef,request):
        try:
            offer_canceled=ServiceProviderOffer.objects.filter(status='C', order__user=request.user)
            serializer=OfferPriceSerializer(offer_canceled,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except ServiceProviderOffer.DoesNotExist:
            return Response({"error": "Offer not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class SubmitRatingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, provider_id):
        try:
            provider = Brovides_services.objects.get(id=provider_id)
            serializer = RatingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user, service_provider=provider)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Brovides_services.DoesNotExist:
            return Response({"error": "مقدم الخدمة غير موجود"}, status=status.HTTP_404_NOT_FOUND)

class SubmitClientRatingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, client_id):
        provider = request.user
        client = get_object_or_404(Cuser, id=client_id)

        data = request.data.copy()
        data['provider'] = provider.id
        data['client'] = client.id

        serializer = ClientRatingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class times_provider(APIView):
    
    def get (slef,request):
        try:

            times=ServiceProviderOffer.objects.filter(status='A',provider=request.user)
            serializer=GET_orders(times,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"eroor":str(e)},status=status.HTTP_400_BAD_REQUEST)






class times_provider_cancel(APIView):
    def get (slef,request):
        if request.user.Provides_services == True:
            return Response ({"error":"user not aloow exist here"},status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                times=ServiceProviderOffer.objects.filter(status='C',provider=request.user)
                serializer=GET_orders(times,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"eroor":str(e)},status=status.HTTP_400_BAD_REQUEST)













from social_django.utils import load_strategy, load_backend
from social_core.exceptions import MissingBackend
from social_core.actions import do_complete


class SocialLoginView(APIView):
    def post(self, request, *args, **kwargs):
        provider = request.data.get('provider', None)
        if provider is None:
            return Response({"error": "Provider is required"}, status=status.HTTP_400_BAD_REQUEST)

        strategy = load_strategy(request)
        try:
            
            backend = load_backend(strategy, provider, None)
        except MissingBackend:
            return Response({"error": "Invalid provider"}, status=status.HTTP_400_BAD_REQUEST)

        access_token = request.data.get('access_token', None)
        if access_token is None:
            return Response({"error": "Access token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = backend.do_auth(access_token)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if user and user.is_active:
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Authentication failed"}, status=status.HTTP_400_BAD_REQUEST)