from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views 



urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/index.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'), 
    path('buy/', views.buy, name='buy'),
    path('item/<int:item_id>/', views.item_details, name='item_details'),  
    path('sell/', views.post_ad, name='sell'),
    path('post-ad/', views.post_ad, name='post_ad'),
    path('My_ads', views.My_ads, name='My_ads'),
    path('update/<int:product_id>', views.update_details, name='update'),
    path('delete/<int:product_id>', views.delete_ad, name='delete'), 
]