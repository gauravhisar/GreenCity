from Home.models import Project
from django.urls import path,include
from Home.views import ProjectViewSet, CustomerViewSet, DealerViewSet, PlotViewSet, DealsFileUploadViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'projects',ProjectViewSet)
router.register(r'customers',CustomerViewSet)
router.register(r'dealers',DealerViewSet)
# router.register(r'upload',DealsFileUploadViewSet,basename = "upload")

urlpatterns = router.urls + [
]
print(urlpatterns)