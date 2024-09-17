from django.contrib import admin
from .models import Cuser, Services, Brovides_services, Rating, ClientRating, Order_service, ServiceProviderOffer, Notfications_Broviders, notfications_client


lista=[
    Cuser,Services,Brovides_services,Rating,ClientRating,Order_service,ServiceProviderOffer,Notfications_Broviders,notfications_client
]
for i in lista:
    admin.site.register(i)
    
    
