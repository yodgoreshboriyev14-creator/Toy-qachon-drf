from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import Guests
from apps.serializers import RegisterModelSerializers, GuestModelSerializer


# Create your views here.

@extend_schema(request=RegisterModelSerializers, responses=RegisterModelSerializers)
class RegisterApiView(APIView):
    def post(self, request):
        serializer = RegisterModelSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': "Ro'yxatdan o'tdingiz"}, status=201)
        return Response(serializer.errors, status=400)


class IndexAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'base/index.html'

    @extend_schema(exclude=True)
    def get(self, request):
        return Response({})

class DashboardAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'dashboard.html'

    @extend_schema(exclude=True)
    def get(self, request):
        return Response({})

@extend_schema(tags=['Guest'])
class GuestListCreateAPIView(ListCreateAPIView):
    serializer_class = GuestModelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['full_name', 'phone_number']
    filterset_fields = ['side', 'status', 'group']
    def get_queryset(self):
        return Guests.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



@extend_schema(tags=['Guest'])
class GuestDetailAPIView(RetrieveDestroyAPIView):
    serializer_class = GuestModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Guests.objects.filter(user=self.request.user)

