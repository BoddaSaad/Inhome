from django.urls import path
from .views import *

urlpatterns = [
    path('sing_up/',SingViewSet.as_view(),name='sing'),
    path('sign_in/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("All_service_in_app/", All_Service_in_app.as_view(), name="all service"),
    path("active_provider/", Brovicevieset.as_view(), name="Brovicevieset"),
    #path('api/social-login/', SocialLoginView.as_view(), name='social-login'),
    path("UserDetailView/",UserDetailView.as_view(),name='UserDetailView'),
    path('resetPassword/',ResetPasswordView.as_view(),name='ResetPasswordView'),
    path('checkCode/',CheckCodeView.as_view(),name='CheckCodeView'),
    path('change_passviwe/',Change_passviwe.as_view(),name='Change_passviwe'),
    # we display all service in wep site
    path('all_service/', Serviceviewset.as_view(), name='all_service'),
    #detals service 
    # استخدام id في الـ URL
    path('order_service/<int:id>/', Orderservicevieset.as_view(), name='order_service'),
    #updata phone _country _ lan
    path('userupdate/', UpdateUserView.as_view(), name='user-update'),
    #display all orders for proivider 
    path("order_service/", Offered_services.as_view()),
    #order detal 
    #post offer
    # updata ofeer after cancel 
    path('order/offers/<int:id>/', detal_service.as_view(), name='service_provider_offer_get'),
    path('order/<int:order_id>/offers/', detal_service.as_view(), name='service_provider_offer_post'),
    path('order/offers/update/<int:offer_id>/', detal_service.as_view(), name='service_provider_offer_put'),

    #all offer display offer to get on client
    path('all-offers/', All_offers.as_view(), name='all_offers'),
    path("beast_offer/", beast_offers.as_view(), name="beast_offers"),
    #accept or refused order 
    path('offer_decision/<int:offer_id>/', OfferDecisionView.as_view(), name='offer_decision'),
    #get all offer accpet
    path('accepted_offers/', AcceptedOffersView.as_view(), name='accepted_offers'),
    
    #get all cancel offer  
    #path('revise_offer/<int:offer_id>/', ReviseOfferAPIView.as_view(), name='revise_offer'),
    
    path('cancel_offer/',Get_canceled_offer.as_view(),name="cancel"),
    path("cancel_offer_provider/", times_provider_cancel.as_view(), name=""),
    #path('rate_service/<int:provider_id>/', SubmitRatingView.as_view(), name='rate_service'),
    #cancel one offer provider
    path('cancel_order/<int:order_id>/', CancelOrderView.as_view(), name='cancel_order'),
    #cancel offer from client 
    path('cancel_offer/<int:offer_id>/', CancelServiceProviderOfferView.as_view(), name='cancel_offer'),
    #rate client     
    path('rate_client/<int:client_id>/', SubmitClientRatingView.as_view(), name='rate_client'),
    #rate provider 
    path('rate_service/<int:provider_id>/', SubmitRatingView.as_view(), name='rate_service'),
    #get provider accep orders
    path('provider_accept/',times_provider.as_view()),
    # updata compleat service
    #################################################################################################################################
    
    
    path("compleat/<int:offer_id>/", Completa_proceser.as_view(), name="completa"),
    # get compleat servicer for provider
    path("Completa_proceser_client/<int:offer_id>/", Completa_proceser_client.as_view(), name="Completa_proceser_client"),
    
    path("Get_compleata_for_provider/",Get_compleata_for_provider.as_view()),
    #get compleat servicer for client
    path("Get_compleata_for_client/", Get_compleata_for_client.as_view(), name="Get_compleata_for_client"),
    path('orders/filter-by-location/', FilterOrdersByProviderLocationView.as_view(), name='filter-orders-by-location'),
    #path('service-provider-offers/', ServiceProviderOfferListView.as_view(), name='service-provider-offers-list'),
    #path('update_offer_price/<int:offer_id>/', UpdateOfferPriceView.as_view(), name='update_offer_price'),
    path("notfications_provider/delete/<int:notif_id>/", Notifications.as_view(), name="delete_notification_provider"),
    path("notfications_client/delete/<int:notif_id>/", Notfi_client.as_view(), name="delete_notification_client"),
    path("notfications_provider/", Notifications.as_view(), name="Notifications"),
    path("notfications_client/", Notfi_client.as_view(), name="Notfi_client"),
    path('vodafone-cash-payment/', VodafoneCashPaymentAPIView.as_view(), name='vodafone-cash-payment'),
    #refused order from provider
    path("refused_order_provider/", Rufesd_order_provider.as_view(),name="refused_order_provider")  ,
    path("currency/", User_currency.as_view(), name="User_currency"),
    path("new_notfications/", new_notfications.as_view(), name="new_notfications"),
    path("new_notfications_brovider/", new_notfications_brovider.as_view(), name="new_notfications_brovider")
    
]
