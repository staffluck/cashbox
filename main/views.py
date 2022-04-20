from django.template.loader import render_to_string
from rest_framework.generics import GenericAPIView

from .serializers import ChequeSerializer

class GenerateChequeAPIView(GenericAPIView):
    serializer_class = ChequeSerializer
