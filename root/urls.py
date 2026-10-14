from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from apps.views import IndexAPIView, DashboardAPIView

urlpatterns = [
        # path('admin/', admin.site.urls),
    path('', IndexAPIView.as_view(), name='home'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/v1/', include('apps.urls')),
    path('dashboard/', DashboardAPIView.as_view(), name='dashboard')
]
