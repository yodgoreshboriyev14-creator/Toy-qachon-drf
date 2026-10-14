from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.views import RegisterApiView, GuestListCreateAPIView, GuestDetailAPIView

urlpatterns = [
   path('register/', RegisterApiView.as_view(), name='register'),
   path('login/', TokenObtainPairView.as_view(), name='login'),
   path('guests/', GuestListCreateAPIView.as_view(), name='guest-list'),
   path('guests/<int:pk>', GuestDetailAPIView.as_view(), name='guest-detail')
]