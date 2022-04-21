from uuid import uuid4
from typing import List
import os

from django.template.loader import render_to_string
from django.utils import timezone
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
import pdfkit
import qrcode
from qrcode.image.svg import SvgPathImage

from .serializers import ChequeIdsSerializer
from .models import Cheque, Item


def generate_qrcode(url: str) -> SvgPathImage:
    factory = SvgPathImage
    img = qrcode.make(url, image_factory=factory)
    return img

def generate_cheque(items: List[Item], template="receipt.html") -> Cheque:
    final_sum = 0  # Раз SQL запрос и так выполнится для получения всех items(для шаблона), использовать aggregate нет смысла(если объектов не много)
    for item in items:
        final_sum += item.price

    now = timezone.now()
    template_string = render_to_string(template, context={"items": items, "final_sum": final_sum, "created_at": now})
    unique_name = uuid4()

    if not os.path.isdir("media/cheques"):
        os.makedirs("media/cheques/")
    file_path = f"cheques/{unique_name}.pdf"
    pdfkit.from_string(template_string, f"media/{file_path}")

    cheque = Cheque.objects.create(cheque=file_path)
    return cheque


class GenerateChequeAPIView(GenericAPIView):
    serializer_class = ChequeIdsSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        items = Item.objects.filter(id__in=serializer.data["items"])
        cheque = generate_cheque(items)
        url_to_cheque = request.build_absolute_uri(cheque.cheque.url)
        qrcode_svg = generate_qrcode(url_to_cheque)

        return HttpResponse(qrcode_svg.to_string(), content_type="image/svg+xml")
