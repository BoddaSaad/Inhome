from django.contrib import admin
from .models import Cuser, Services, Brovides_services, Rating, ClientRating, Order_service, ServiceProviderOffer, Notfications_Broviders, notfications_client ,Send_offer_from_provider
from .utils import send_to_device

class BrovidesServicesInline(admin.StackedInline):  # You can also use TabularInline
    model = Brovides_services

class CuserAdmin(admin.ModelAdmin):
    inlines = [BrovidesServicesInline]

    exclude = ('fcm', 'password', 'name')
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        for field_name, field in form.base_fields.items():
            field.required = False
        return form

    def save_model(self, request, obj, form, change):
        if change:  # Check if this is an update
            user = Cuser.objects.get(pk=obj.pk)
            old_status = user.is_active
            new_status = obj.is_active
            if not old_status and new_status:  # Status changed to active                
                # Send FCM notification
                fcm = user.fcm  # Replace with the actual field name for the FCM token
                if fcm:
                    send_to_device(
                        fcm,
                        "Account Activated",
                        "Your account has been activated. You can now log in and use the app."
                    )
        super().save_model(request, obj, form, change)

admin.site.register(Cuser, CuserAdmin)

class Brovides_servicesAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "Provided Service"
        verbose_name_plural = "Provided Services"

admin.site.register(Brovides_services, Brovides_servicesAdmin)

admin.site.register(Services)

# lista=[
#     Services,Rating,ClientRating,Order_service,ServiceProviderOffer,Notfications_Broviders,notfications_client,Send_offer_from_provider
# ]
# for i in lista:
#     admin.site.register(i)
    