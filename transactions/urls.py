from . import views                                                                
from django.urls import path                                                       
                                                                                   
urlpatterns = [                                                                    
    path('', views.TransactionsView.as_view(), name='root'),
    path('upload', views.TransactionsFileUploadFormView.as_view(), name='root.upload'),
    path('<str:ticker>/', views.TransactionDetailView.as_view(), name='root.detail'),
]

