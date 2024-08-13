from django.urls import path
from .views import *

urlpatterns = [

    path('api/social-login/', SocialLoginView.as_view(), name='social-login'),
    path('resetPassword/',ResetPasswordView.as_view(),name='ResetPasswordView'),
    path('checkCode',CheckCodeView.as_view(),name='CheckCodeView'),
    path('change_passviwe',CheckCodeView.as_view(),name='Change_passviwe'),
    path('all_service',Serviceviewset.as_view(),'all_service'),
    path('order_service',Orderservicevieset.as_view(),'order_service'),
    path('userupdate/<int:id>/', CuserUpdateView.as_view(), name='user-update'),
    path('user/update/<int:id>/', CuserUpdateView_2.as_view(), name='user-update'),
    path("offer_service", Offered_services, name='offer'),
    path('order/<int:order_id>/offers/', detal_service.as_view(), name='service_provider_offer'),
    path('all-offers/', All_offers.as_view(), name='all_offers'),
    path('offer_decision/<int:offer_id>/', OfferDecisionView.as_view(), name='offer_decision'),
    path('accepted_offers/', AcceptedOffersView.as_view(), name='accepted_offers'),
    path('cancel_offer/',Get_canceled_offer.as_view(),name="cancel"),
    path('rate_service/<int:provider_id>/', SubmitRatingView.as_view(), name='rate_service'),
    path('cancel_offer/<int:offer_id>/', CancelServiceProviderOfferView.as_view(), name='cancel_offer'),
     path('rate_client/<int:client_id>/', SubmitClientRatingView.as_view(), name='rate_client'),
  path('rate_service/<int:provider_id>/', SubmitRatingView.as_view(), name='rate_service'),
]