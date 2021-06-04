from Home.models import Project
from django.urls import path,include
from Home import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'projects',views.ProjectViewSet)
router.register(r'customers',views.CustomerViewSet)
router.register(r'dealers',views.DealerViewSet)
router.register(r'plots',views.PlotViewSet)
router.register(r'deals',views.DealViewSet)
router.register(r'project/upload',views.DealsFileUploadViewSet,basename = "upload")

# plot_router = routers.DefaultRouter()
# plot_router.register(r'plots',ProjectDetailsViewSet, basename = 'plot-project-detail')

urlpatterns = router.urls + [
    
]