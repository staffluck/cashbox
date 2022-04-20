from uuid import uuid4

import pdfkit
from django.template.loader import render_to_string
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from .serializers import ChequeIdsSerializer
from .models import Item

def generate_cheque(items: Item, template="receipt.html") -> str:
    final_sum = 0  # Раз SQL запрос и так выполнится для получения всех items(для шаблона), использовать aggregate нет смысла(если объектов не много)
    for item in items:
        final_sum += item.price

    template_string = render_to_string(template, context={"items": items, "final_sum": final_sum})
    unique_name = uuid4()
    pdfkit.from_string(template_string, f"media/cheques/{unique_name}.pdf")


class GenerateChequeAPIView(GenericAPIView):
    serializer_class = ChequeIdsSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        items = Item.objects.filter(id__in=serializer.data["ids"])
        generate_cheque(items)

        return Response(serializer.data)
