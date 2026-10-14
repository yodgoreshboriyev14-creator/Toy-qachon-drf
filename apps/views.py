from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from apps.serializers import RegisterModelSerializers


# Create your views here.

@extend_schema(request=RegisterModelSerializers, responses=RegisterModelSerializers)
class RegisterApiView(APIView):
    def post(self, request):
        serializer = RegisterModelSerializers(data=request.data)
        if serializer.is_valid():
            user = serializer.save()




