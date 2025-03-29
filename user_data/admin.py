from django.contrib import admin
from .models import Cuser, Services, Brovides_services, Rating, ClientRating, Order_service, ServiceProviderOffer, Notfications_Broviders, notfications_client ,Send_offer_from_provider
from .utils import send_to_device

class CuserAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if change:  # Check if this is an update
            old_status = Cuser.objects.get(pk=obj.pk).is_active
            new_status = obj.is_active
            if not old_status and new_status:  # Status changed to active                
                # Send FCM notification
                fcm = obj.fcm  # Replace with the actual field name for the FCM token
                if fcm:
                    send_to_device(
                        fcm,
                        "Account Activated",
                        "Your account has been activated. You can now log in and use the app."
                    )
        super().save_model(request, obj, form, change)


lista=[
    Cuser,Services,Brovides_services,Rating,ClientRating,Order_service,ServiceProviderOffer,Notfications_Broviders,notfications_client,Send_offer_from_provider
]
for i in lista:
    admin.site.register(i, CuserAdmin)
    