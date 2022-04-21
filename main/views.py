from uuid import uuid4
from typing import List

from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
import pdfkit
import qrcode

from .serializers import ChequeIdsSerializer
from .models import Cheque, Item


def generate_qrcode(url: str) -> str:
    img = qrcode.make(url)
    unique_name = uuid4()
    file_path = f"qrcodes/{unique_name}.png"
    img.save(f"media/{file_path}")
    return file_path

def generate_cheque(items: List[Item], template="receipt.html") -> Cheque:
    final_sum = 0  # Раз SQL запрос и так выполнится для получения всех items(для шаблона), использовать aggregate нет смысла(если объектов не много)
    for item in items:
        final_sum += item.price

    now = timezone.now()
    template_string = render_to_string(template, context={"item1": items[0], "item2": items[1], "final_sum": final_sum, "created_at": now})
    unique_name = uuid4()
    file_path = f"cheques/{unique_name}.pdf"
    pdfkit.from_string(template_string, f"media/{file_path}")

    cheque = Cheque.objects.create(cheque=file_path)
    return cheque


class GenerateChequeAPIView(GenericAPIView):
    serializer_class = ChequeIdsSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        items = Item.objects.filter(id__in=serializer.data["ids"])
        cheque = generate_cheque(items)
        url_to_cheque = request.build_absolute_uri(cheque.cheque.url)
        qrcode_path = generate_qrcode(url_to_cheque)
        cheque.qrcode = qrcode_path

        url_to_qrcode = request.build_absolute_uri(cheque.qrcode.url)
        return Response(url_to_qrcode)
