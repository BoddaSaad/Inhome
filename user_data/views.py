from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .serializers import SingUpSerializer
from .models import *
from .serializers import *
import random
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
User = get_user_model()
class SingViewSet(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        serializer = SingUpSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully", "user_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

##
class Brovicevieset(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = Brovice_data(data=data)
            if serializer.is_valid():
                brovice = serializer.save()
                return Response({"account": "is active now"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)




def generate_random_code(length=6):
    code = ''.join(random.choices('0123456789', k=length))
    return code
    
class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    
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
    permission_classes = [AllowAny]
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
    permission_classes = [AllowAny]
    
    def post(self,request):
        data=request.data 
        serializer=Change_password(data=data)
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
    permission_classes = [AllowAny]
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
    
    
    def get_permissions(self):
        """
        تخصيص الأذونات بناءً على نوع الطلب (GET أو POST)
        """
        if self.request.method == 'GET':
            # السماح للجميع (بما في ذلك المستخدمين غير المصادقين) باستخدام GET
            return [AllowAny()]
        # السماح فقط للمستخدمين المصادقين باستخدام POST
        return [IsAuthenticated()]
    
    
    
    

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
    
        if request.user.Provides_services==True:
            return Response({
                "hi":"You are not allowed to be here"
            })
        else:
            
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


    

class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            user = Cuser.objects.get(email=request.user.email)  # Get the current user
            serializer = CombinedCuserSerializer(user, data=request.data)  # Pass the user instance and data
            
            if serializer.is_valid():  # Validate the data
                serializer.save()  # Save the changes
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return validation errors if any
        except Cuser.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Offered_services(APIView):
    permission_classes=[IsAuthenticated]
    def get (slef,request):
        if request.user.is_active==False:
            return Response({
                "please":"Please pay the debt"
            })
        if request.user.Provides_services==True:
            try:
                offer=Order_service.objects.all()
                serializer=Order_serviceserlizer(offer,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "eroor":"this site not aloow for you"
            })

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
        if request.user.Provides_services==False:
            return Response({"hi":"You are not allowed to be here"})
        else:
            try:
                order = Order_service.objects.get(id=order_id)
                provider = request.user
                data = request.data
                data['order'] = order.id
                data['provider'] = provider.id
                data['status'] = 'P'  
                serializer = ServiceProviderOfferSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except IntegrityError:
                return Response({"error": "You have already submitted an offer for this order."}, status=400)

                        
            
            
    def put(self, request, offer_id):
        try:
            offer = ServiceProviderOffer.objects.get(id=offer_id)
            data = request.data
            data['status'] = 'P'  
            serializer = ServiceProviderOfferSerializer_put(offer, data=data, partial=True)
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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # تصفية العروض بناءً على المستخدم الحالي
            offers = ServiceProviderOffer.objects.filter(order__user=request.user.id).exclude(status='R')
            serializer = OfferPriceSerializer(offers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class OfferDecisionView(APIView):
    permission_classes = [IsAuthenticated]
    # def get(self,request):
    #     try:
    #         offers=ServiceProviderOffer.objects.filter(order__user=request.id).exclude(status='R')
    #         serializer=Offers(offers,many=True)
    #         return Response(serializer.data,status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({
    #             "eroor":str(e)
    #         })
        

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
        if request.user.Provides_services==True:
            return Response({"eroor":"not allow for you "})
        else:
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
        if request.user.Provides_services==True:
            return Response(
               {
                   "hi":"not aloow for you"
            })
        else:
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
        if request.user.Provides_services==True:
            return Response({
                "eroor":"not aloow for you"
            })
        else:
            
            try:
                provider = Brovides_services.objects.get(user__id=provider_id)
                data = request.data.copy()
                data['service_provider']=provider.id
                serializer = RatingSerializer(data=data)
                if Rating.objects.filter(service_provider=provider, user=request.user).exists():
                    return Response({"error": "لقد قمت بالفعل بتقييم هذا مقدم الخدمة."}, status=status.HTTP_400_BAD_REQUEST)

                if serializer.is_valid():
                    serializer.save(user=request.user, service_provider=provider)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Brovides_services.DoesNotExist:
                return Response({"error": "مقدم الخدمة غير موجود"}, status=status.HTTP_404_NOT_FOUND)

class SubmitClientRatingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, client_id):
        if request.user.Provides_services==False:
            return Response( {
                "hi":"not allow for you"
            })
            
        else:     
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
        if request.user.Provides_services == False:
            return Response ({"error":"user not aloow exist here"},status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                times=ServiceProviderOffer.objects.filter(status='A',provider=request.user)
                serializer=GET_orders(times,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"eroor":str(e)},status=status.HTTP_400_BAD_REQUEST)






class times_provider_cancel(APIView):
    def get (slef,request):
        if request.user.Provides_services == False:
            return Response ({"error":"user not aloow exist here"},status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                times=ServiceProviderOffer.objects.filter(status='C',provider=request.user)
                serializer=GET_orders(times,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"eroor":str(e)},status=status.HTTP_400_BAD_REQUEST)


class Notifications(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.Provides_services==False:
            return Response(
                "not allow for you"
            )
        try:
            # جلب جميع الإشعارات المتعلقة بالمزود الذي قام بتسجيل الدخول
            notifications = Notfications_Broviders.objects.filter(brovider=request.user.id)
            
            # تحويل البيانات باستخدام Serializer المناسب (يجب أن تكون قد قمت بإنشاء Serializer للإشعارات)
            serializer = Noticationserlizer(notifications, many=True)
            
            # إرجاع البيانات في استجابة HTTP
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)








class CancelOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, order_id):
        if request.user.Provides_services==True:
            try:
                # الحصول على الطلب (Order) بناءً على معرف الطلب
                #order = get_object_or_404(Order_service, id=order_id)
                
                # التحقق من أن المستخدم الذي يقوم بالطلب هو مقدم الخدمة المرتبط بالطلب
                provider_offer = ServiceProviderOffer.objects.filter(id=order_id, provider=request.user).first()
                
                if not provider_offer:
                    return Response({"error": "You are not authorized to cancel this order."}, status=status.HTTP_403_FORBIDDEN)
                
                # تحديث حالة العرض إلى 'Canceled' 
                if provider_offer.status=='C':
                    return Response("offer canceled already" ,status=status.HTTP_226_IM_USED)
                
                provider_offer.status = 'C'
                provider_offer.save()
                
                # إنشاء إشعار للعميل
                notification = notfications_client.objects.create(
                    title="Order Canceled",
                    content=f"Your order for service '{provider_offer.order.service.name}' has been canceled by the provider.",
                    user=provider_offer.order.user
                )
                
                # إرسال الإشعار (يمكنك تخصيص هذا بناءً على متطلباتك)
                # هنا يتم إرجاع الإشعار مباشرة كجزء من الرد
                serializer = NotificationSerializer_clent(notification)
                return Response({"message": "Order has been canceled and notification sent.", "notification": serializer.data}, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'eroor':'not allow for you'},status=status.HTTP_202_ACCEPTED)
        
class Notfi_client(APIView):
    def get(self,request):
        if request.user.Provides_services==True:
            return Response(
                "not allow for you"
            )
        try:
            notif=notfications_client.objects.filter(user=request.user.id)
            serializer=NotificationSerializer_clent(notif,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"eroor":str(e)},status=status.HTTP_400_BAD_REQUEST)
        

class Get_compleata_for_provider(APIView):
    
    def get(self,request):
        if request.user.Provides_services==False:
            return Response({"eroor":"you not aloow"})
        else:
            try:
                services_offers=ServiceProviderOffer.objects.filter(provider=request.user,status='Complete')
                
                serializer=CompleatService(services_offers,many=True)
                
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                    
                )
            except Exception as e :
                return Response(
                    {"eroor":str(e) },            
                    status=status.HTTP_400_BAD_REQUEST 
                )



class Get_compleata_for_client(APIView):
    
    def get(self,request):
        if request.user.Provides_services==True:
            return Response({"eroor":"you not aloow"})
        else:
            try:
                services_offers=ServiceProviderOffer.objects.filter(order__user=request.user,status='Complete')
                
                serializer=CompleatService(services_offers,many=True)
                
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                    
                )
            except Exception as e :
                return Response(
                    {"eroor":str(e) },            
                    status=status.HTTP_400_BAD_REQUEST 
                )








class ServiceProviderOfferListView(APIView):
    permission_classes = [IsAuthenticated]
     
    def get(self, request, *args, **kwargs):
        if request.user.Provides_services==True:
            return Response({"eroor":"you not aloow"})
        else:
            offers = ServiceProviderOffer.objects.filter(order__user=request.user,status='Complete')
            serializer = CompleatService(offers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)






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
        
        
        
class UpdateOfferPriceView(APIView):
    def put(self, request, offer_id):
        try:
            offer = ServiceProviderOffer.objects.get(id=offer_id)
        except ServiceProviderOffer.DoesNotExist:
            return Response({"error": "Offer not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ServiceProviderOfferUpdateSerializer(offer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ReviseOfferAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, offer_id):
        try:
            offer = ServiceProviderOffer.objects.get(id=offer_id)

            # تحديث العرض بالحالة الجديدة وغيرها من المعلومات
            serializer = OfferUpdateSerializer(offer, data=request.data, partial=True)
            if serializer.is_valid():
                # تعيين الحالة إلى "Revised"
                serializer.save(status='V')
                return Response({"success": "Offer revised successfully"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ServiceProviderOffer.DoesNotExist:
            return Response({"error": "Offer not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
class Completa_proceser(APIView):
    def put(self, request, offer_id):
        if request.user.is_active==False:
            return Response({
                "please":"Please pay the debt"
            })
        if request.user.Provides_services:
            try:
                # الحصول على العرض والتحقق من وجوده
                offer = ServiceProviderOffer.objects.get(id=offer_id)
                
                # التحقق مما إذا كان العرض مكتمل بالفعل
                if offer.status == "Complete":
                    return Response({"message": "This offer is already complete."})
                
                # تحديث حالة العرض إلى "Complete"
                offer.status = 'Complete'
                offer.save()
                
                # تحديث مديونية مقدم الخدمة
                provider = Brovides_services.objects.get(user=request.user)
                price_offer = int(offer.price)
                provider.indebtedness += price_offer
                provider.save()
                
                # إنشاء إشعار لمقدم الخدمة
                Notfications_Broviders.objects.create(
                    title="الرجاء تسديد الرسوم المطلوبة",
                    content="اذهب هنا للمحفظة",
                    brovider=request.user
                )

                return Response(status=status.HTTP_200_OK)
                
            except ServiceProviderOffer.DoesNotExist:
                return Response({"error": "Offer not found."}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "You are not allowed to perform this action."}, status=status.HTTP_403_FORBIDDEN)


class Completa_proceser_client(APIView):
    def put(self, request, offer_id):
        if request.user.request_services:
            try:
                # الحصول على العرض والتحقق من وجوده
                offer = ServiceProviderOffer.objects.get(id=offer_id)
                
                # التحقق مما إذا كان العرض مكتمل بالفعل
                if offer.status == 'Complete':
                    return Response({"message": "This offer is already complete."})
                
                # تحديث حالة العرض إلى "Complete"
                offer.status = 'Complete'
                offer.save()
                
                provider = Brovides_services.objects.get(user=offer.provider)
                price_offer = int(offer.price)
                provider.indebtedness += price_offer
                provider.save()

                
                # إنشاء إشعار لمقدم الخدمة
                Notfications_Broviders.objects.create(
                    title="الرجاء تسديد الرسوم المطلوبة",
                    content="اذهب هنا للمحفظة",
                    brovider=provider.user
                )
                
                return Response({"done":"done"},status=status.HTTP_200_OK)
                
            except ServiceProviderOffer.DoesNotExist:
                return Response({"error": "Offer not found."}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "You are not allowed to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        
        
        
        
        
        
        
        
        
        
        
import requests
from rest_framework_simplejwt.tokens import RefreshToken
class GoogleLoginView(APIView):
    def get_user_info(self, access_token):
        user_info_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}
        user_info_response = requests.get(user_info_url, headers=headers)
        return user_info_response.json()
    
    def post(self, request, *args, **kwargs):
        code = request.data.get('code')    
        
        # Exchange the authorization code for an access token
        token_url = 'https://oauth2.googleapis.com/token'
        client_id = '297166509341-2a60tih8cq8co20bbq83gr4kg5fkd372.apps.googleusercontent.com'
        client_secret = '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'
        redirect_uri = 'http://localhost:5173/'  # This should match the redirect URI you used for Google OAuth
        payload = {
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
        }

        # Make a POST request to exchange the code for a token
        response = requests.post(token_url, data=payload)
        token_data = response.json()

        if 'access_token' in token_data:
            # Fetch user info from Google
            user_info = self.get_user_info(token_data['access_token'])

            # Check if the user already exists, if not, create a new user
            user, created = Cuser.objects.get_or_create(
                email=user_info['email'], 
                defaults={
                    'username': user_info['name'],
                    'Provides_services': False,  # Default value, can be adjusted
                    'request_services': True,    # Default value, can be adjusted
                    'phone': '',                 # You can update this with actual phone info if available
                    'country': '',               # Add logic to fetch the country if needed
                }
            )

            # Generate JWT token
            refresh = RefreshToken.for_user(user)

            # Add additional data to the access token payload
            refresh.payload['full_name'] = user.username  # Adjust if you have a 'full_name' field
            refresh.payload['email'] = user.email
            refresh.payload['vendor_id'] = user.vendor.id if hasattr(user, 'vendor') else 0

            return Response({
                'status': 'success', 
                'message': 'Google login successful', 
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Failed to authenticate with Google'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
        
        
    
        
        
        
# class VodafoneCashPaymentAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
        
#         indebtednes=Brovides_services.objects.get(user=request.user)
#         amount=indebtednes.indebtedness
#         user=request.user
#         print(amount)
        
        
        
        
#         # Step 1: Auth Token
#         auth_token_response = requests.post(settings.PAYMOB_AUTH_URL, json={
#             "api_key": settings.PAYMOB_API_KEY
#         })
#         if auth_token_response.status_code != 201:
#             return Response({"error": "Authentication failed"}, status=status.HTTP_400_BAD_REQUEST)

#         auth_token = auth_token_response.json().get("token")

#         # Step 2: Create Order
#         print("llllllllllllllllllll")
#         order_response = requests.post(settings.PAYMOB_ORDER_URL, json={
#             "auth_token": auth_token,
#             "delivery_needed": "false",
#             "amount": int(amount),  
#             "currency": "EGP",
#             "expiration": 5800,
#             "payment_methods": [122, "’Mobile"],
#             "items": [
#                 {
#                     "name": "service",
#                     "amount": int(amount),
#                     "description": "service",
#                     "quantity": 1
#                 }
#             ]
#         })
#         if order_response.status_code != 201 :
#             return Response({"error": "Order creation failed"}, status=status.HTTP_400_BAD_REQUEST)

#         order_data = order_response.json()
#         order_id = order_data.get("id")

#         # Step 3: Payment Key
#         print("llllllllllllllllllll")
#         payment_key_response = requests.post(settings.PAYMOB_PAYMENT_KEY_URL, json={
#             "auth_token": auth_token,
#             "amount_cents": request.data.get('amount_cents', 10000),  # Default amount for testing
#             "expiration": 3600,
#             "order_id": order_id,
#             "billing_data": {
#                 "apartment": "803",  # Default apartment for testing
#                 "email": user.email,  # Default email for testing
#                 "floor": "1",  # Default floor for testing
#                 "first_name": user.username,  # Default first name for testing
#                 "street": "Main St",  # Default street for testing
#                 "building": "123",  # Default building for testing
#                 "phone_number": user.phone,  # Default phone number for testing
#                 "shipping_method": "PKG",  # Default shipping method
#                 "postal_code": "12345",  # Default postal code for testing
#                 "city": "Cairo",  # Default city for testing
#                 "country": "EG",  # Default country
#                 "last_name": "Doe",  # Default last name for testing
#                 "state": "Cairo"  # Default state for testing
#             },
#             "currency": "EGP",
#             "integration_id": settings.PAYMOB_INTEGRATION_ID
#         })
#         if payment_key_response.status_code != 201:
#             return Response({"error": "Failed to create payment key"}, status=status.HTTP_400_BAD_REQUEST)

#         payment_token = payment_key_response.json().get("token")

#         # Step 4: Redirect URL
#         payment_url = f"{settings.PAYMOB_IFRAME_URL}{settings.PAYMOB_IFRAME_ID}?payment_token={payment_token}"

#         return Response({"payment_url": payment_url}, status=status.HTTP_200_OK)
    
    
    


class VodafoneCashPaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        indebtednes=Brovides_services.objects.get(user=request.user)
        amount=indebtednes.indebtedness
        user=request.user
       
        
        
        
        
        
        auth_token_response = requests.post(settings.PAYMOB_AUTH_URL, json={
            "api_key": settings.PAYMOB_API_KEY
        })
        if auth_token_response.status_code != 201:
            return Response({"error": "Authentication failed"}, status=status.HTTP_400_BAD_REQUEST)

        auth_token = auth_token_response.json().get("token")

        # Step 2: Create Order
        order_response = requests.post(settings.PAYMOB_ORDER_URL, json={
            "auth_token": auth_token,
            "delivery_needed": "false",
            "amount_cents": int(amount*100),  # Default amount for testing
            "currency": "EGP",
           # "merchant_order_id": request.data.get('order_id', '12345'),  # Default order ID for testing
            "items": [
                
                {
                     "name": "service",
                     "amount_cents": int(amount*100),
                     "description": "service",
                     "quantity": 1
                }
                
            ]
        })
        
        if order_response.status_code != 201:
            return Response({"error": "Order creation failed"}, status=status.HTTP_400_BAD_REQUEST)

        order_data = order_response.json()
        order_id = order_data.get("id")

        # Step 3: Payment Key
        payment_key_response = requests.post(settings.PAYMOB_PAYMENT_KEY_URL, json={
            "auth_token": auth_token,
            "amount_cents": int(amount*100),  # Default amount for testing
            "expiration": 3600,
            "order_id": order_id,
            "billing_data": {
                "apartment": "803",  # Default apartment for testing
                "email": user.email,  # Default email for testing
                "floor": "1",  # Default floor for testing
                "first_name": user.username,  # Default first name for testing
                "street": "Main St",  # Default street for testing
                "building": "123",  # Default building for testing
                "phone_number": user.phone,  # Default phone number for testing
                "shipping_method": "PKG",  # Default shipping method
                "postal_code": "12345",  # Default postal code for testing
                "city": "Cairo",  # Default city for testing
                "country": "EG",  # Default country
                "last_name": "Doe",  # Default last name for testing
                "state": "Cairo"  # Default state for testing
            },
            "currency": "EGP",
            "integration_id": settings.PAYMOB_INTEGRATION_ID
        })
        if payment_key_response.status_code != 201:
            return Response({"error": "Failed to create payment key"}, status=status.HTTP_400_BAD_REQUEST)

        payment_token = payment_key_response.json().get("token")

        # Step 4: Redirect URL
        payment_url = f"{settings.PAYMOB_IFRAME_URL}{settings.PAYMOB_IFRAME_ID}?payment_token={payment_token}"

        return Response({"payment_url": payment_url}, status=status.HTTP_200_OK)