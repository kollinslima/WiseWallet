from . import views                                                                
from django.urls import path                                                       
                                                                                   
urlpatterns = [                                                                    
    path('', views.TransactionsFileUploadFormView.as_view(), name='transactions'),                               
    path('upload/success', views.TransactionsFileUploadSuccessView.as_view(), name='transactions.upload.success'),                               
] 

