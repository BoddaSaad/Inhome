from django.urls import path
from .views import *

urlpatterns = [
    path('sing_up/',SingViewSet.as_view(),name='sing'),
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
    path("Get_compleata_for_provider/",Get_compleata_for_provider.as_view()),
    #get compleat servicer for client
    
    path('service-provider-offers/', ServiceProviderOfferListView.as_view(), name='service-provider-offers-list'),
    path('update_offer_price/<int:offer_id>/', UpdateOfferPriceView.as_view(), name='update_offer_price'),
    path('vodafone-cash-payment/', VodafoneCashPaymentAPIView.as_view(), name='vodafone-cash-payment'),
  
]
