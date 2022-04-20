from django.urls import path

from .views import GenerateChequeAPIView

urlpatterns = [
    path('cash_machine/', GenerateChequeAPIView.as_view(), ),
]
