from django.template.loader import render_to_string
from rest_framework.generics import GenericAPIView

from .serializers import ChequeSerializer

class GenerateChequeAPIView(GenericAPIView):
    serializer_class = ChequeSerializer

    def post(self, request):
        serializer = self.get_serializer(request.data)
        serializer.is_valid(raise_exception=True)

        return serializer.data
