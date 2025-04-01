from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views 



urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/index.html'), name='login'),  #login page
    path('logout/', LogoutView.as_view(template_name='accounts/index.html'), name='logout'), #logout page
    path('signup/', views.signup, name='signup'), #sign-up page
    path('dashboard/', views.dashboard, name='dashboard'),  #dashboard page
    path('buy/', views.buy, name='buy'),  #buy page
    path('item/<int:item_id>/', views.item_details, name='item_details'),  #item details page
    path('sell/', views.post_ad, name='sell'),  #seller page
    path('post-ad/', views.post_ad, name='post_ad'),  #post ad page
    path('My_ads', views.My_ads, name='My_ads'),  # my ads page
    path('update/<int:product_id>', views.update_details, name='update'),  #ads updation page
    path('delete/<int:product_id>', views.delete_ad, name='delete'),  #ads deletion page
]