from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contracts/', views.contracts, name='contracts'),
    path('new_contract/', views.new_contract, name='new_contract'),
    path('state_change/', views.state_change, name='state_change'),
    path('terminate/', views.terminate, name='terminate'),
    path('revoke/', views.revoke, name='revoke'),
    path('org_request/', views.org_request, name='org_request'),
    path('org_contracts/', views.org_contracts, name='org_contracts'),
    path('reject_req/', views.reject_req, name='reject_req'),
    path('accept_req/', views.accept_req, name='accept_req'),
    path('view_data/', views.view_data, name='view_data'),
    path('release/', views.release, name='release'),
    path('recent_activity/', views.recent_activity, name='recent_activity'),

]
