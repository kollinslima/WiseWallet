from . import views                                                                
from django.urls import path                                                       

app_name = "authentication"
urlpatterns = [                                                                    
    path('', views.LoginView.as_view(), name='index'),                               
    path('signup/', views.SignupView.as_view(), name='index.signup'),                               
    path('logout/', views.LogoutView.as_view(), name='index.logout'),                               
] 

