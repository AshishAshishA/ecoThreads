from django.urls import path
from .views import (dashboard, createOrder, reviewOrder, updateOrder, deleteOrder,
                    myOrders, allauth_login, allauth_signup, get_areas, map_view, 
                    staff_dashboard, orders_list, update_status)
from allauth.account import views as auth_views

urlpatterns = [
    #customer section
    path('', dashboard, name='dashboard'),
    path('create/', createOrder, name='create-order'),
    path('review/<int:pk>', reviewOrder, name='review-order'),
    path('update/<int:pk>', updateOrder, name='update-order'),
    path('delete/<int:pk>', deleteOrder, name='delete-order'),
    path('myorders/', myOrders, name='my-orders'),
    path('get_areas/<int:city_id>/', get_areas, name='get_areas'),


    #staff section
    path('staff/', staff_dashboard, name='staff_dashboard'),
    path('staff/orderlist/', orders_list, name='orders_list'),
    path('staff/orderlist/<str:status>', orders_list, name='orders_pending'),
    path('staff/orderlist/<str:status>', orders_list, name='orders_out_to_collect'),
    path('staff/orderlist/<str:status>', orders_list, name='orders_collected'),
    path('staff/update/status/<int:pk>', update_status, name='update_status'),

    path('map/', map_view, name='map_view'),
    path('map/<str:status>', map_view, name='pending'),
    path('map/<str:status>', map_view, name='out_to_collect'),
    path('map/<str:status>', map_view, name='collected'),


    #verification section
    path('accounts/login/', allauth_login, name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/signup/', allauth_signup, name='signup'),

    path('accounts/password/reset/', auth_views.PasswordResetView.as_view(), name='account_reset_password'),
    # Change password
    path('accounts/password/change/', auth_views.PasswordChangeView.as_view(), name='account_change_password'),

    path('email/', auth_views.EmailView.as_view(), name='account_email'),
    path('email/sent/', auth_views.EmailVerificationSentView.as_view(), name='account_email_verification_sent'),
    path('confirm-email/', auth_views.ConfirmEmailView.as_view(), name='account_confirm_email'),
]