from django.contrib import admin
from .models import Cuser, Services, Brovides_services, Rating, ClientRating, Order_service, ServiceProviderOffer, Notfications_Broviders, notfications_client ,Send_offer_from_provider


lista=[
    Cuser,Services,Brovides_services,Rating,ClientRating,Order_service,ServiceProviderOffer,Notfications_Broviders,notfications_client,Send_offer_from_provider
]
for i in lista:
    admin.site.register(i)
    
    
