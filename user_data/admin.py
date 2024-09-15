from django.contrib import admin
from .models import Cuser, Services, Brovides_services, Rating, ClientRating, Order_service, ServiceProviderOffer, Notfications_Broviders, notfications_client

@admin.register(Cuser)
class CuserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'country', 'location', 'lan', 'Provides_services', 'request_services')
    search_fields = ('username', 'email', 'phone', 'country')
    list_filter = ('Provides_services', 'request_services', 'lan')

@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ('name', 'photo', 'detal')
    search_fields = ('name',)

@admin.register(Brovides_services)
class Brovides_servicesAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'rating')
    search_fields = ('user__username', 'service__name')
    list_filter = ('rating',)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('service_provider', 'user', 'rating', 'comment', 'created_at')
    search_fields = ('service_provider__user__username', 'user__username', 'comment')
    list_filter = ('rating', 'created_at')

@admin.register(ClientRating)
class ClientRatingAdmin(admin.ModelAdmin):
    list_display = ('client', 'provider', 'rating', 'comment', 'created_at')
    search_fields = ('client__username', 'provider__username', 'comment')
    list_filter = ('rating', 'created_at')

@admin.register(Order_service)
class Order_serviceAdmin(admin.ModelAdmin):
    list_display = ('service', 'user', 'type_service', 'time', 'location', 'file', 'count')
    search_fields = ('service__name', 'user__username', 'type_service', 'location')
    list_filter = ('time', 'location')

@admin.register(ServiceProviderOffer)
class ServiceProviderOfferAdmin(admin.ModelAdmin):
    list_display = ('time_arrive', 'order', 'provider', 'price', 'comment', 'created_at', 'status')
    search_fields = ('order__service__name', 'provider__username', 'comment', 'status')
    list_filter = ('status', 'created_at')

@admin.register(Notfications_Broviders)
class Notfications_BrovidersAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'brovider')
    search_fields = ('title', 'content', 'brovider__username')

@admin.register(notfications_client)
class Notfications_clientAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'user')
    search_fields = ('title', 'content', 'user__username')
