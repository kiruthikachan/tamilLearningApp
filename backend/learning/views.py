from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Letter
from .serializers import letterSerializer

# Create your views here.

@api_view(["GET"])
def letter_list(request):
    letters = Letter.objects.filter(is_active = True).order_by("display_order")

    serializer = letterSerializer(letters,many=True)

    return Response(serializer.data)