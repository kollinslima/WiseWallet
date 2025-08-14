from . import views                                                                
from django.urls import path                                                       
                                                                                   
app_name = "transactions"
urlpatterns = [                                                                    
    path('', views.TransactionsView.as_view(), name='index'),
    path('upload', views.TransactionsFileUploadFormView.as_view(), name='index.upload'),
    path('detail/<str:ticker>', views.TransactionDetailView.as_view(), name='index.detail'),
]

