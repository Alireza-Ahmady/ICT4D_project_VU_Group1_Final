from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import Malaria_caseViewSet, register_case, calculate_risk, check_malaria_cases
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .admin import MyAdminSite

router = DefaultRouter()
router.register(r'malaria_cases', Malaria_caseViewSet)

my_admin_site = MyAdminSite()

urlpatterns = [
    path('register_case/', register_case, name='register_case'),
    path('calculate_risk/', calculate_risk, name='calculate_risk'),
    path('check_malaria_cases/', check_malaria_cases, name='check_malaria_cases'),
]

urlpatterns += router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
