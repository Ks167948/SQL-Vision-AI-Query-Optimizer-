from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, QueryAnalysisViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'analyze', QueryAnalysisViewSet)

urlpatterns = [
    path('', include(router.urls)),
]