from django.db.models import base
from Home.models import Project
from django.urls import path,include
from Home import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'projects',views.ProjectViewSet)
router.register(r'customers',views.CustomerViewSet)
router.register(r'dealers',views.DealerViewSet)

plots_router = routers.DefaultRouter()
plots_router.register(r'plots',views.PlotViewSet,basename='plot')

deals_router = routers.DefaultRouter()
deals_router.register(r'deals',views.DealViewSet, basename='deal')

dues_router = routers.DefaultRouter()
dues_router.register(r'dues',views.DueViewSet,basename = 'due')
payments_router = routers.DefaultRouter()
payments_router.register(r'payments',views.PaymentViewSet, basename = 'payment')
commissions_router = routers.DefaultRouter()
commissions_router.register(r'commissions',views.CommissionPaymentViewSet, basename='commission_payment')

router.register(r'projects/<project_id>/upload',views.DealsFileUploadViewSet,basename = "upload")

urlpatterns = router.urls + [
    path('projects/<int:project_id>/',include(deals_router.urls)),
    path('projects/<int:project_id>/', include(plots_router.urls)),
    path('projects/<int:project_id>/deals/<int:deal_id>/', include(dues_router.urls)),
    path('projects/<int:project_id>/deals/<int:deal_id>/', include(payments_router.urls)),
    path('projects/<int:project_id>/deals/<int:deal_id>/', include(commissions_router.urls)),
]
